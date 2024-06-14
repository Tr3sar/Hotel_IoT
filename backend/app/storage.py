from sqlalchemy.orm import Session, joinedload
from app import models, schemas

from app.SmartClient.SmartClient import SmartClient
from app.SmartRoom.SmartRoom import SmartRoom
from app.SmartServices.Restaurant import RestaurantService
from app.SmartServices.Spa import SpaService
from app.Staff.CleaningStaff import CleaningStaff

class Storage:
    def __init__(self):
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
            if reservation.reservation_type == "restaurant":
                self.reservations[reservation.id] = RestaurantService(reservation.id, reservation.client_id, reservation.time)
            elif reservation.reservation_type == "spa":
                self.reservations[reservation.id] = SpaService(reservation.id, reservation.client_id, reservation.time)

        room_assignments = db.query(models.RoomAssignment).all()
        for assignment in room_assignments:
            self.room_assignments[assignment.id] = assignment

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

    def get_cleaning_staff(self, staff_id: int):
        return self.cleaning_staff.get(staff_id)

    def create_cleaning_staff(self, db: Session, staff: schemas.CleaningStaffCreate):
        db_staff = models.CleaningStaff(name=staff.name)
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        self.cleaning_staff[db_staff.id] = db_staff
        return db_staff

    def get_reservations(self, skip: int = 0, limit: int = 10):
        return list(self.reservations.values())[skip:skip + limit]

    def create_reservation(self, db: Session, reservation: schemas.ReservationCreate):
        db_reservation = models.Reservation(client_id=reservation.client_id, reservation_type=reservation.reservation_type, time=reservation.time)
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        self.reservations[db_reservation.id] = db_reservation
        return db_reservation

    def get_room_assignment(self, assignment_id: int):
        return self.room_assignments.get(assignment_id)

    def create_room_assignment(self, db: Session, assignment: schemas.RoomAssignmentCreate):
        db_assignment = models.RoomAssignment(client_id=assignment.client_id, room_id=assignment.room_id)
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        self.room_assignments[db_assignment.id] = db_assignment
        return db_assignment

    def check_in(self, db: Session, client_id: int, room_number: int):
        db_assignment = models.RoomAssignment(client_id=client_id, room_id=room_number)
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        self.room_assignments[db_assignment.id] = db_assignment
        return db_assignment

    def check_out(self, db: Session, client_id: int, room_number: int):
        db_assignment = db.query(models.RoomAssignment).filter_by(client_id=client_id, room_id=room_number).first()
        if db_assignment:
            db.delete(db_assignment)
            db.commit()
            del self.room_assignments[db_assignment.id]
        return db_assignment
