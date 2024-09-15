from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from fastapi import HTTPException

from app.SmartHotel.SmartHotel import SmartHotel
from app.SmartClient.SmartClient import SmartClient
from app.SmartRoom.SmartRoom import SmartRoom, RoomStatus
from app.SmartServices.Restaurant.RestaurantService import RestaurantService
from app.SmartServices.Spa.SpaService import SpaService
from app.Staff.CleaningStaff.CleaningStaff import CleaningStaff
from app.Staff.SecurityStaff.SecurityStaff import SecurityStaff

from app.schemas import StaffRole

import schedule
import threading
import time
from datetime import datetime, timedelta
from faker import Faker
import random
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
        self.staff = {}
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
            timestamp = datetime.now()
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
            self.rooms[room.id] = SmartRoom(room.id, room.number, room.status)
        
        clients = db.query(models.Client).all()
        for client in clients:
            self.clients[client.id] = SmartClient(client.id, client.first_name, client.last_name, client.email)
        
        room_assignments = db.query(models.RoomAssignment).all()
        for assignment in room_assignments:
            if assignment.check_out_date is None:
                room_number = self.rooms[assignment.room_id].number
                self.clients[assignment.client_id].checkin(assignment.rfid_code, room_number)
            
        staff = db.query(models.Staff).all()
        for staff_member in staff:
            if "cleaning" in staff_member.role.value:
                self.staff[staff_member.id] = CleaningStaff(staff_member.id, staff_member.name, staff_member.working)
            elif "security" in staff_member.role.value:
                self.staff[staff_member.id] = SecurityStaff(staff_member.id, staff_member.name, staff_member.working)
            if staff_member.working:
                self.staff[staff_member.id].start_shift()
        
        tasks = db.query(models.Task).all()
        for task in tasks:
            staff_member = self.staff.get(task.staff_id)
            room_number = self.rooms[task.room_id].number

            staff_member.assign_task(room_number)

        #Revisar
        reservations = db.query(models.Reservation).all()
        for reservation in reservations:
            self.clients[reservation.client_id].make_reservation(reservation.type, reservation.start_date)

    def populate_db(self, db: Session):
        fake = Faker('es_ES')

        
        clients = []
        for _ in range(10):
            client = models.Client(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                postal_code=fake.postcode(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                id_document_type=random.choice(["passport", "driver_license", "national_id"]),
                id_document_number=fake.unique.ssn()
            )
            clients.append(client)
        db.add_all(clients)
        db.commit()


        rooms = []
        for i in range(1, 21):
            randomtype = random.choice(["single", "double", "suite"])
            room = models.Room(
                number=i,
                type=randomtype,
                status=random.choice(["available", "occupied", "maintenance"]),
                price=random.uniform(80.0, 300.0),
                floor=random.randint(1, 3),
                description=fake.text(max_nb_chars=200),
                max_occupancy= 1 if randomtype == "single" else 4,
                last_maintenance=datetime.now()-timedelta(hours=random.randint(1, 12))
            )
            rooms.append(room)
        db.add_all(rooms)
        db.commit()


        room_assignments = []
        assigned_rooms = set()
        for client in clients:
            available_rooms = [room for room in rooms if room.id not in assigned_rooms]
            if not available_rooms:
                break
        
            assigned_room = random.choice(available_rooms)
            available_rooms.append(assigned_room.id)

            room_assignment = models.RoomAssignment(
                client_id=client.id,
                room_id=assigned_room.id,
                rfid_code=random.randint(1000, 9999),
                check_in_date=datetime.now() - timedelta(days=random.randint(1, 5)),
                check_out_date=None,
                expense=0.0
            )
            room_assignments.append(room_assignment)
        db.add_all(room_assignments)
        db.commit()

        
        devices = []
        for room in rooms:
            ac_device = models.Device(
                room_id=room.id,
                type="AC",
                value=22
            )
            bulb_device = models.Device(
                room_id=room.id,
                type="Bulb",
                value=100
            )
            devices.extend([ac_device, bulb_device])
        db.add_all(devices)
        db.commit()

        
        electricity_consumptions = []
        for assignment in room_assignments:
            for _ in range(10):
                consumption = models.ElectricityConsumption(
                    room_assignment_id=assignment.id,
                    timestamp=datetime.now() - timedelta(hours=random.randint(1, 48)),
                    consumption=random.uniform(0.0, 3.0) * 30
                )
                electricity_consumptions.append(consumption)
        db.add_all(electricity_consumptions)
        db.commit()

        
        water_consumptions = []
        for assignment in room_assignments:
            for _ in range(10):
                consumption = models.WaterConsumption(
                    room_assignment_id=assignment.id,
                    timestamp=datetime.now() - timedelta(hours=random.randint(1, 48)),
                    consumption=random.uniform(8.0, 225.0) / 7.5
                )
                water_consumptions.append(consumption)
        db.add_all(water_consumptions)
        db.commit()

        
        staff = []
        roles = ["cleaning", "security"]
        for _ in range(10):
            staff_member = models.Staff(
                name=fake.name(),
                role=random.choice(roles),
                working=random.choice([True, False]),
                salary=random.uniform(20000.0, 50000.0),
                phone_number=fake.phone_number(),
                email=fake.unique.email(),
                shift_schedule=fake.json()
            )
            staff.append(staff_member)
        db.add_all(staff)
        db.commit()

        
        tasks = []
        for staff_member in staff:
            if staff_member.role == "cleaning" and staff_member.working is True:
                for _ in range(5):
                    task = models.Task(
                        staff_id=staff_member.id,
                        room_id=random.choice(rooms).id,
                        task_status=random.choice(["pending", "in_progress", "completed"]),
                        assigned_at=datetime.now() - timedelta(hours=random.randint(1, 24)),
                        completed_at=datetime.now() if random.choice([True, False]) else None
                    )
                    tasks.append(task)
        db.add_all(tasks)
        db.commit()

        
        reservations = []
        for client in clients:
            reservation = models.Reservation(
                client_id=client.id,
                type=random.choice(["restaurant", "spa"]),
                start_date=datetime.now() - timedelta(days=random.randint(1, 10)),
                end_date=datetime.now() + timedelta(days=random.randint(1, 5)),
                status=random.choice(["confirmed", "cancelled", "in_process"]),
                payment_status=random.choice(["pending", "paid"]),
                total_cost=random.uniform(100.0, 500.0),
                special_request=fake.sentence(nb_words=6)
            )
            reservations.append(reservation)
        db.add_all(reservations)
        db.commit()

        print("Database populated with sample data.")

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

    def get_rooms(self, db: Session, skip: int = 0, limit: int = 50):
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

    def trigger_smoke_detection(self, room_id: int):
        """
        room_id = None
        for rid, room in self.rooms.items():
            if room.number == room_number:
                room_id = rid
                break
        """
        
        if room_id not in self.rooms.keys():
            raise HTTPException(status_code=404, detail="Room not found")
        
        room = self.rooms.get(room_id)
        if room and room.smoke_sensor:
            room.smoke_sensor.trigger_smoke_detection()
        else:
            raise ValueError("No smoke sensor found for this room.")

    #RoomAssignment
    def get_room_assignment(self, db: Session, assignment_id: int):
        return db.query(models.RoomAssignment).filter(models.RoomAssignment.id == assignment_id).first()
    
    def get_room_assignments(self, db: Session, skip: int = 0, limit: int = 50):
        return db.query(models.RoomAssignment).offset(skip).limit(limit).all()
    
    def create_room_assignment(self, db: Session, assignment: schemas.RoomAssignmentCreate):
        db_room = db.query(models.Room).filter(models.Room.id == assignment.room_id).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        db_client = db.query(models.Client).filter(models.Client.id == assignment.client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        try:
            db_assignment = models.RoomAssignment(client_id=db_client.id, room_id=db_room.id, rfid_code=assignment.rfid_code, check_in_date=assignment.check_in_date, check_out_date=assignment.check_out_date, expense=assignment.expense)
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
    
    def update_check_out_time(self, db: Session, room_assignment_id: int):
        room_assignment = db.query(models.RoomAssignment).filter(models.RoomAssignment.id == room_assignment_id).first()
        
        if not room_assignment:
            return None
        
        room_assignment.check_out_date = datetime.now()
        db.commit()
        db.refresh(room_assignment)
        
        return room_assignment

    def get_room_assignment_consumption(self, db: Session, room_assignment_id: int):
        room_assignment = db.query(models.RoomAssignment).filter(models.RoomAssignment.id == room_assignment_id).first()
        if not room_assignment:
            return None
        
        client_electricity_consumptions = db.query(models.ElectricityConsumption).filter(models.ElectricityConsumption.room_assignment_id == room_assignment_id).all()
        client_water_consumptions = db.query(models.WaterConsumption).filter(models.WaterConsumption.room_assignment_id == room_assignment_id).all()

        electricity_consumptions = db.query(models.ElectricityConsumption).all()
        water_consumptions = db.query(models.WaterConsumption).all()

        if len(electricity_consumptions) == 0: 
            total_current_average = 0.0
        else:
            total_current_average = sum([c.consumption for c in electricity_consumptions]) / len(electricity_consumptions)

        if len(water_consumptions) == 0:
            total_flow_rate_average = 0.0
        else:
            total_flow_rate_average = sum([c.consumption for c in water_consumptions]) / len(water_consumptions)

        if len(client_electricity_consumptions) == 0:
            client_current_average = 0.0
        else:
            client_current_average = sum([c.consumption for c in client_electricity_consumptions]) / len(client_electricity_consumptions)

        if len(client_water_consumptions) == 0:
            client_flow_rate_average = 0.0
        else:
            client_flow_rate_average = sum([c.consumption for c in client_water_consumptions]) / len(client_water_consumptions)
        
        return {
            "client_current_average": client_current_average,
            "client_flow_rate_average": client_flow_rate_average,
            "total_current_average": total_current_average,
            "total_flow_rate_average": total_flow_rate_average
        }
    
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
        
        room_id = None
        for room_assignment in self.rooms.values():
            if room_assignment.occupied_by == client_id:
                room_id = room_assignment.get_id()
                break
        
        if room_id is None:
            raise ValueError("Room not found")
        smart_client.requestRoomCleaning(room_id)
        return {'message': 'Cleaning requested successfully'}
 
    def order_restaurant(self, client_id: int, order_details: str):
        client = self.get_client(client_id)
        if not client:
            raise ValueError("Client not found")
        client.order_restaurant(order_details)
    
    def make_reservation(self, client_id: int, reservation: schemas.ReservationCreate):
        smart_client = self.clients.get(client_id)
        if not smart_client:
            raise ValueError("Client not found")
        smart_client.make_reservation(reservation.type, reservation.start_date)

    #Staff
    
    def get_staff(self, db: Session, skip: int = 0, limit: int = 50):
        return db.query(models.Staff).offset(skip).limit(limit).all()

    def get_staff_by_id(self, staff_id: int):
        return self.staff.get(staff_id)

    def create_staff(self, db: Session, staff: schemas.StaffCreate):
        db_staff = models.Staff(
            name=staff.name,
            role=staff.role,
            working=staff.working,
            salary=staff.salary,
            phone_number=staff.phone_number,
            email=staff.email,
            shift_schedule=staff.shift_schedule
        )
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        self.staff[db_staff.id] = db_staff
        return db_staff

    def update_staff(self, db: Session, staff_id: int, staff: schemas.Staff):
        db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
        if not db_staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        
        db_staff.name = staff.name
        db_staff.role = staff.role
        db_staff.working = staff.working
        db_staff.salary = staff.salary
        db_staff.phone_number = staff.phone_number
        db_staff.email = staff.email
        db_staff.shift_schedule = staff.shift_schedule
        
        db.commit()
        db.refresh(db_staff)
        return db_staff
    
    def update_shift_status(self, db: Session, staff_id: int, working: bool):
        db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
        if not db_staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        
        db_staff.working = working

        db.commit()
        db.refresh(db_staff)

        return db_staff
        
    def start_shift(self, staff_id: int):
        
        staff_member = self.staff.get(staff_id)
        if not staff_member:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        staff_member.start_shift()
        return {"id": staff_id, "name": staff_member.name, "working": staff_member.working}

    def end_shift(self, staff_id: int):
        staff_member = self.staff.get(staff_id)
        if not staff_member:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        staff_member.end_shift()
        return {"id": staff_id, "name": staff_member.name, "working": staff_member.working}

    def start_task(self, staff_id: int, room_id: int):
        staff_member = self.staff.get(staff_id)
        if not staff_member:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        staff_member.start_task(self.rooms[room_id].number)
        return {"id": staff_id, "name": staff_member.name, "working": staff_member.working}

    def complete_task(self, staff_id: int, room_id: int):
        staff_member = self.staff.get(staff_id)
        if not staff_member:
            raise HTTPException(status_code=404, detail="Cleaning staff not found")
        
        staff_member.complete_task(self.rooms[room_id].number)
        
        return {"id": staff_id, "name": staff_member.name, "working": staff_member.working}

    #Task
    def create_task(self, db: Session, task: schemas.TaskCreate):
        db_task = models.Task(
            task_status=task.task_status,
            assigned_at=task.assigned_at,
            completed_at=task.completed_at,
            staff_id=task.staff_id,
            room_id=task.room_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get_task_by_id(self, db: Session, task_id: int):
        return db.query(models.Task).filter(models.Task.id == task_id).first()
    
    def get_tasks_by_staff_id(self, db: Session, staff_id: int):
        return db.query(models.Task).filter(models.Task.staff_id == staff_id).all()

    def get_tasks(self, db: Session, skip: int = 0, limit: int = 50):
        return db.query(models.Task).offset(skip).limit(limit).all()

    def update_task(self, db: Session, task_id: int, task: schemas.Task):
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not db_task:
            return None
        db_task.task_status = task.task_status
        db_task.assigned_at = task.assigned_at
        db_task.completed_at = task.completed_at
        db_task.staff_id = task.staff_id
        db_task.room_id = task.room_id
        db.commit()
        db.refresh(db_task)
        return db_task

    def delete_task(self, db: Session, task_id: int):
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not db_task:
            return None
        db.delete(db_task)
        db.commit()
        return db_task

    #Reservation
    def get_reservations(self, db: Session, skip: int = 0, limit: int = 50):
        return db.query(models.Reservation).offset(skip).limit(limit).all()

    def get_reservation(self, db: Session, reservation_id: int):
        return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    def create_reservation(self, db: Session, reservation: schemas.ReservationCreate):
        try:
            if reservation.type not in ["restaurant", "spa"]:
                raise HTTPException(status_code=400, detail="Invalid reservation type")
            
            smart_client = self.clients.get(reservation.client_id)
            if not smart_client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            db_reservation = models.Reservation(client_id=reservation.client_id, type=reservation.type, start_date=reservation.start_date, end_date=reservation.end_date, status=reservation.status, payment_status=reservation.payment_status, total_cost=reservation.total_cost, special_request=reservation.special_request)

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