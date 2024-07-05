from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from fastapi import HTTPException

from app.SmartHotel.SmartHotel import SmartHotel
from app.SmartClient.SmartClient import SmartClient
from app.SmartRoom.SmartRoom import SmartRoom, RoomStatus
from app.SmartServices.Restaurant.RestaurantService import RestaurantService
from app.SmartServices.Spa.SpaService import SpaService
from app.Staff.CleaningStaff.CleaningStaff import CleaningStaff

import schedule
import threading
import time
import datetime
from app.database import SessionLocal

import logging

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self):
        self.hotel = SmartHotel()
        self.restaurant = RestaurantService()
        self.spa = SpaService()
        
        self.rooms = {}
        self.clients = {}
        self.cleaning_staff = {}
        self.reservations = {}

        schedule.every().hour.do(self.save_accumulated_data)

        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.start()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def save_accumulated_data(self):
        db = SessionLocal()
        try:
            timestamp = datetime.datetime.now()
            for room in self.rooms.values():
                self.record_light_consumption(db, room.get_number(), room.occupied_by, room.electricity_consumption_sensor.get_consumption_data(), timestamp)
                self.record_water_consumption(db, room.get_number(), room.occupied_by, room.water_flow_sensor.get_flow_rate_sum(), timestamp)

                room.electricity_consumption_sensor.clear_consumption_data()
                room.water_flow_sensor.clear_flow_rate_sum()
        finally:
            db.close()

    def load_from_db(self, db: Session):
        rooms = db.query(models.Room).all()
        for room in rooms:
            self.rooms[room.id] = SmartRoom(room.id, room.number)
        
        clients = db.query(models.Client).all()
        for client in clients:
            self.clients[client.id] = SmartClient(client.id, client.name, client.email)
        
        room_assignments = db.query(models.RoomAssignment).all()
        for assignment in room_assignments:
            room_number = self.rooms[assignment.room_id].number
            self.clients[assignment.client_id].checkin(assignment.rfid_code, room_number)
        
        cleaning_staff = db.query(models.CleaningStaff).all()
        for staff in cleaning_staff:
            self.cleaning_staff[staff.id] = CleaningStaff(staff.id, staff.name, staff.working)
            if staff.working:
                self.cleaning_staff[staff.id].start_shift()

        #Revisar
        reservations = db.query(models.Reservation).all()
        for reservation in reservations:
            self.clients[reservation.client_id].make_reservation(reservation.id, reservation.reservation_type, reservation.start_date)

    #Hotel
    def notify_event(self, event_info: str):
        self.hotel.notify_event(event_info)

    #Sensor
    def record_light_consumption(self, db: Session, room_number: int, client_id: int, consumption: float, timestamp: datetime):
        db_consumption = models.ElectricityConsumption(room_number=room_number, client_id=client_id, consumption=consumption, timestamp=timestamp)
        db.add(db_consumption)
        db.commit()
        db.refresh(db_consumption)
        return db_consumption

    def record_water_consumption(self, db: Session, room_number: int, client_id: int, consumption: float, timestamp: datetime):
        db_consumption = models.WaterConsumption(room_number=room_number, client_id=client_id, consumption=consumption, timestamp=timestamp)
        db.add(db_consumption)
        db.commit()
        db.refresh(db_consumption)
        return db_consumption
    
    #Room
    def get_room(self, room_id: int):
        return self.rooms.get(room_id)

    def get_room_by_number(self, db: Session, number: int):
        return db.query(models.Room).filter(models.Room.number == number).first()

    def create_room(self, db: Session, room: schemas.RoomCreate):
        db_room = models.Room(number=room.number, status=room.status)
        db.add(db_room)
        db.commit()
        db.refresh(db_room)

        ac_device = models.Device(room_id=db_room.id, type="AC", value=22)
        bulb_device = models.Device(room_id=db_room.id, type="Bulb", value=100)
        
        db.add(ac_device)
        db.add(bulb_device)
        db.commit()
        db.refresh(ac_device)
        db.refresh(bulb_device)

        self.rooms[db_room.id] = db_room
        return db_room

    def get_rooms(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Room).offset(skip).limit(limit).all()
    
    def update_room_devices(self, db: Session, room_id: int, temperature: int, lighting_intensity: int):
        room = self.rooms.get(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        ac_device = db.query(models.Device).filter_by(room_id=room_id, type="AC").first()
        bulb = db.query(models.Device).filter_by(room_id=room_id, type="Bulb").first()

        if not ac_device:
            raise HTTPException(status_code=404, detail="AC Device not found")

        if not bulb:
            raise HTTPException(status_code=404, detail="Light Device not found")
        
        ac_device.value = temperature
        bulb.value = lighting_intensity

        db.commit()
        db.refresh(ac_device)
        db.refresh(bulb)
        
        logger.info(f"Room {room.number}: Temp={ac_device.value}, LI={bulb.value}")

        return {"AC": ac_device.value, "Bulb": bulb.value}
    
    def update_room_status(self, db: Session, room_number: int, status: str):
        logger.info(f"Updating room {room_number} status to {status}")
        db_room = db.query(models.Room).filter(models.Room.number == room_number).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")

        if status not in [status.value for status in RoomStatus]:
            raise HTTPException(status_code=400, detail="Invalid room status")

        db_room.status = status

        db.add(db_room)
        db.commit()
        db.refresh(db_room)

        return db_room
    
    def adjust_environment(self, room_number: int, temperature: int, lighting_intensity: int):
        room_id = None
        for rid, room in self.rooms.items():
            if room.number == room_number:
                room_id = rid
                break

        if room_id is None:
            raise HTTPException(status_code=404, detail="Room not found")

        client_id = self.rooms[room_id].get_occupied_by()
        
        smart_client = self.get_client(client_id)
        if not smart_client:
            raise ValueError("Client not found")

        smart_client.adjust_environment(temperature, lighting_intensity)

        return {"AC": temperature, "Bulb": lighting_intensity}

    def trigger_smoke_detection(self, room_number: int):
        room_id = None
        for rid, room in self.rooms.items():
            if room.number == room_number:
                room_id = rid
                break

        if room_id is None:
            raise HTTPException(status_code=404, detail="Room not found")
        
        room = self.rooms.get(room_id)
        if room and room.smoke_sensor:
            room.smoke_sensor.trigger_smoke_detection()
        else:
            raise ValueError("No smoke sensor found for this room.")

    #RoomAssignment
    def get_room_assignment(self, db: Session, assignment_id: int):
        return db.query(models.RoomAssignment).filter(models.RoomAssignment.id == assignment_id).first()
    
    def get_room_assignments(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.RoomAssignment).offset(skip).limit(limit).all()
    
    def create_room_assignment(self, db: Session, assignment: schemas.RoomAssignmentCreate):
        db_room = db.query(models.Room).filter(models.Room.id == assignment.room_id).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        db_client = db.query(models.Client).filter(models.Client.id == assignment.client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        try:
            db_assignment = models.RoomAssignment(client_id=db_client.id, room_id=db_room.id, rfid_code=assignment.rfid_code)
            db.add(db_assignment)
            db.commit()
            db.refresh(db_assignment)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Room or RFID code already assigned")
        
        return db_assignment

    def delete_room_assignment(self, db: Session, assignment_id: int):
        db_assignment = db.query(models.RoomAssignment).filter(models.RoomAssignment.id == assignment_id).first()
        if not db_assignment:
            return None
        db.delete(db_assignment)
        db.commit()
        return db_assignment
    
    #Client
    def get_client(self, client_id: int):
        return self.clients.get(client_id)

    def create_client(self, db: Session, client: schemas.ClientCreate):
        db_client = models.Client(name=client.name, email=client.email, rfid_code=client.rfid_code, room_number=client.room_number)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        self.clients[db_client.id] = db_client
        return db_client

    def get_clients(self, db: Session, skip: int = 0, limit: int = 20):
        return db.query(models.Client).offset(skip).limit(limit).all()
    
    def check_in(self, client_id: int, rfid_code: int, room_number: int):
        smart_client = self.clients.get(client_id)

        if not smart_client:
            raise HTTPException(status_code=404, detail="Client not found")

        smart_room = None
        for room in self.rooms.values():
            if room.number == room_number:
                smart_room = room
                break
                
        if not smart_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        if room.occupied_by is not None:
            raise HTTPException(status_code=400, detail="Room is already occupied")
        
        smart_client.checkin(rfid_code, room_number)

        return {"message": "Client checked in successfully"}

    def check_out(self, client_id: int, rfid_code: int, room_number: int):
        smart_room = None
        for room in self.rooms.values():
            if room.number == room_number:
                smart_room = room
                break
                
        if not smart_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        if room.occupied_by is not client_id:
            raise HTTPException(status_code=400, detail="Room not occupied by this client")
        
        if not client_id in self.clients.keys():
                raise HTTPException(status_code=404, detail="Client not found")
        
        smart_client = self.clients.get(client_id)
        smart_client.checkout()
        return {"message": "Client checked out successfully"}

    def request_cleaning(self, client_id: int):
        smart_client = self.get_client(client_id)
        if not smart_client:
            raise ValueError("Client not found")
        elif smart_client.getRoom() is None:
            raise ValueError("Client is not checked in")
                    
        smart_client.requestRoomCleaning()
        return {'message': 'Cleaning requested successfully'}
 
    def order_restaurant(self, client_id: int, order_details: str):
        client = self.get_client(client_id)
        if not client:
            raise ValueError("Client not found")
        client.order_restaurant(order_details)
    
    #Cleaning staff

    def get_cleaning_staff(self, staff_id: int):
        return self.cleaning_staff.get(staff_id)

    def create_cleaning_staff(self, db: Session, staff: schemas.CleaningStaffCreate):
        db_staff = models.CleaningStaff(name=staff.name)
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        self.cleaning_staff[db_staff.id] = db_staff
        return db_staff

    def update_cleaning_staff(self, db: Session, staff_id: int, staff: schemas.CleaningStaff):
        db_staff = db.query(models.CleaningStaff).filter(models.CleaningStaff.id == staff_id).first()
        if not db_staff:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        db_staff.name = staff.name
        db_staff.working = staff.working
        db.commit()
        db.refresh(db_staff)
        return db_staff
    
    def start_shift(self, staff_id: int):
        
        cleaning_staff = self.cleaning_staff.get(staff_id)
        if not cleaning_staff:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        cleaning_staff.start_shift()
        return {"id": staff_id, "name": cleaning_staff.name, "working": cleaning_staff.working}

    def end_shift(self, staff_id: int):
        cleaning_staff = self.cleaning_staff.get(staff_id)
        if not cleaning_staff:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        cleaning_staff.end_shift()
        return {"id": staff_id, "name": cleaning_staff.name, "working": cleaning_staff.working}
        
    def complete_task(self, staff_id: int):
        cleaning_staff = self.cleaning_staff.get(staff_id)
        if not cleaning_staff:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        cleaning_staff.complete_task()
        return {"id": staff_id, "name": cleaning_staff.name, "working": cleaning_staff.working}

    #Reservation
    def get_reservations(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Reservation).offset(skip).limit(limit).all()

    def get_reservation(self, db: Session, reservation_id: int):
        return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    def create_reservation(self, db: Session, reservation: schemas.ReservationCreate):
        try:
            if reservation.reservation_type not in ["restaurant", "spa"]:
                raise HTTPException(status_code=400, detail="Invalid reservation type")
            
            db_reservation = models.Reservation(client_id=reservation.client_id, reservation_type=reservation.reservation_type, start_date=reservation.start_date)
            db.add(db_reservation)
            db.commit()
            db.refresh(db_reservation)
            self.reservations[db_reservation.id] = db_reservation
            
            smart_client = self.clients.get(reservation.client_id)
            if not smart_client:
                raise HTTPException(status_code=404, detail="Client not found")
        
            smart_client.make_reservation(db_reservation.id, reservation.reservation_type, reservation.start_date)

            return db_reservation
        except IntegrityError as e:
            db.rollback()
            if "unique_client_time" in str(e.orig):
                raise HTTPException(
                    status_code=400,
                    detail="A reservation for this client already exists at the specified start date."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred."
                )