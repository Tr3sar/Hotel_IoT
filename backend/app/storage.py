from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from fastapi import HTTPException

from app.SmartHotel.SmartHotel import SmartHotel
from app.SmartClient.SmartClient import SmartClient
from app.SmartRoom.SmartRoom import SmartRoom, RoomStatus
from app.SmartServices.Restaurant.RestaurantService import RestaurantService
from app.SmartServices.Spa.SpaService import SpaService
from app.Staff.CleaningStaff import CleaningStaff

import logging

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self):
        self.hotel = SmartHotel()
        self.rooms = {}
        self.clients = {}
        self.cleaning_staff = {}
        self.reservations = {}
        self.room_assignments = {}

    def load_from_db(self, db: Session):
        rooms = db.query(models.Room).all()
        for room in rooms:
            self.rooms[room.id] = SmartRoom(room.number)
        
        clients = db.query(models.Client).options(joinedload(models.Client.reservations)).all()
        for client in clients:
            self.clients[client.id] = SmartClient(client.id, client.name, client.email)
        
        cleaning_staff = db.query(models.CleaningStaff).all()
        for staff in cleaning_staff:
            self.cleaning_staff[staff.id] = CleaningStaff(staff.id, staff.name)

        reservations = db.query(models.Reservation).all()
        for reservation in reservations:
            self.clients[reservation.client_id].make_reservation(reservation.id, reservation.reservation_type, reservation.start_date)

        room_assignments = db.query(models.RoomAssignment).all()
        for assignment in room_assignments:
            #self.room_assignments[assignment.id] = assignment
            room_number = self.rooms[assignment.room_id].number
            self.clients[assignment.client_id].checkin(assignment.rfid_code, room_number)

    #Hotel
    def notify_event(self, event_info: str):
        self.hotel.notify_event(event_info)

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
        self.rooms[db_room.id] = db_room
        return db_room

    def get_rooms(self, skip: int = 0, limit: int = 10):
        return list(self.rooms.values())[skip:skip + limit]
    
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

        if db_room.id in self.rooms:
            self.rooms[db_room.id].status = status
            self.rooms[db_room.id].notifyRoomStatus(status)

        return db_room
    
    def adjust_environment(self, db: Session, client_id: int, temperature: int, lighting_intensity: int):
        smart_client = self.get_client(client_id)
        if not smart_client:
            raise ValueError("Client not found")
        elif smart_client.getRoom() is None:
            raise ValueError("Client is not checked in")
        
        db_room = db.query(models.Room).filter(models.Room.number == smart_client.getRoom()).first()
        if not db_room or db_room.id not in self.rooms:
            raise HTTPException(status_code=404, detail="Room not found")

        ac_device = db.query(models.Device).filter_by(room_id=db_room.id, type="AC").first()
        bulb = db.query(models.Device).filter_by(room_id=db_room.id, type="Bulb").first()

        if not ac_device:
            raise HTTPException(status_code=404, detail="AC Device not found")

        if not bulb:
            raise HTTPException(status_code=404, detail="Light Device not found")

        ac_device.value = temperature
        bulb.value = lighting_intensity

        db.commit()
        db.refresh(ac_device)
        db.refresh(bulb)

        smart_client.adjust_environment(temperature, lighting_intensity)
        logger.info(f"Room {db_room.number}: Temp={ac_device.value}, LI={bulb.value}")

        return {"AC": ac_device, "Bulb": bulb}

    #Client
    def get_client(self, client_id: int):
        return self.clients.get(client_id)

    def create_client(self, db: Session, client: schemas.ClientCreate):
        db_client = models.Client(name=client.name, email=client.email, rfid_code=client.rfid_code, room_number=client.room_number)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        self.clients[db_client.id] = db_client
        print(self.clients)
        print(self.clients[db_client.id])
        return db_client

    def get_clients(self, skip: int = 0, limit: int = 10):
        return list(self.clients.values())[skip:skip + limit]
    
    def check_in(self, db: Session, client_id: int, rfid_code: int, room_number: int):
        logger.info(f"Checking in client {client_id} to room {room_number} with RFID {rfid_code}")

        smart_client = self.clients.get(client_id)

        if not smart_client:
            raise HTTPException(status_code=404, detail="Client not found")

        db_room = db.query(models.Room).filter(models.Room.number == room_number).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        db_assignment = models.RoomAssignment(client_id=client_id, room_id=db_room.id, rfid_code=rfid_code)
        
        try:
            db.add(db_assignment)
            db.commit()
            db.refresh(db_assignment)

            self.room_assignments[db_assignment.id] = db_assignment
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Room or RFID code already assigned")

        smart_client.checkin(db_assignment.rfid_code, room_number)

        return db_assignment

    def check_out(self, db: Session, client_id: int, rfid_code: int, room_number: int):
        logger.info(f"Checking out client {client_id} from room {room_number} with RFID {rfid_code}")
        db_room = db.query(models.Room).filter(models.Room.number == room_number).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        db_assignment = db.query(models.RoomAssignment).filter_by(client_id=client_id, room_id=db_room.id, rfid_code=rfid_code).first()
        if db_assignment:
            db.delete(db_assignment)
            db.commit()
            del self.room_assignments[db_assignment.id]

            smart_client = self.clients.get(client_id)
            smart_client.checkout()
        return db_assignment

    def request_cleaning(self,db: Session, client_id: int):
        smart_client = self.get_client(client_id)
        if not smart_client:
            raise ValueError("Client not found")
        elif smart_client.getRoom() is None:
            raise ValueError("Client is not checked in")
        
        db_room = db.query(models.Room).filter(models.Room.number == smart_client.getRoom()).first()
        try:
            db_room.status = RoomStatus.CLEAN_REQUIRED.value
            db.add(db_room)
            db.commit()
            db.refresh(db_room)

            self.rooms[db_room.id].status = RoomStatus.CLEAN_REQUIRED.value
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Could not request cleaning for room")
            
        smart_client.requestRoomCleaning()
        return {'message': 'Cleaning requested successfully'}

        #To implement
    
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

    #Reservation
    def get_reservations(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.Reservation).offset(skip).limit(limit).all()

    def get_reservation(self, db: Session, reservation_id: int):
        return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    def create_reservation(self, db: Session, reservation: schemas.ReservationCreate):
        logger.info(f"Creating reservation for client {reservation.client_id}, type {reservation.reservation_type} at {reservation.start_date}")
        try:
            db_reservation = models.Reservation(client_id=reservation.client_id, reservation_type=reservation.reservation_type, start_date=reservation.start_date)
            db.add(db_reservation)
            db.commit()
            db.refresh(db_reservation)
            self.reservations[db_reservation.id] = db_reservation
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

    #Room assignment
    #(Change to check-in, check-out)   ?????
    def get_room_assignment(self, assignment_id: int):
        return self.room_assignments.get(assignment_id)

    def create_room_assignment(self, db: Session, assignment: schemas.RoomAssignmentCreate):
        db_assignment = models.RoomAssignment(client_id=assignment.client_id, room_id=assignment.room_id)
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        self.room_assignments[db_assignment.id] = db_assignment
        return db_assignment