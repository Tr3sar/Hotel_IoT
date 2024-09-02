from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class IDDocumentType(enum.Enum):
    passport = 'passport'
    driver_license = 'driver_license'
    national_id = 'national_id'

class RoomType(enum.Enum):
    single = 'single'
    double = 'double'
    suite = 'suite'

class RoomStatus(enum.Enum):
    available = 'available'
    occupied = 'occupied'
    maintenance = 'maintenance'

class ReservationStatus(enum.Enum):
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    in_process = 'in_process'

class PaymentStatus(enum.Enum):
    pending = 'pending'
    paid = 'paid'

class DeviceType(enum.Enum):
    AC = 'AC'
    Bulb = 'Bulb'

class StaffRole(enum.Enum):
    cleaning = 'cleaning'
    security = 'security'
    maintenance = 'maintenance'

class TaskStatus(enum.Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(50))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    date_of_birth = Column(Date)
    id_document_type = Column(Enum(IDDocumentType))
    id_document_number = Column(String(50))
    
    reservations = relationship("Reservation", back_populates="client")
    room_assignments = relationship("RoomAssignment", back_populates="client")


class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(Integer, unique=True, index=True)
    type = Column(Enum(RoomType))
    status = Column(Enum(RoomStatus))
    price = Column(Float)
    floor = Column(Integer)
    description = Column(String)
    max_occupancy = Column(Integer)
    last_maintenance = Column(Date)
    
    devices = relationship("Device", back_populates="room")
    room_assignments = relationship("RoomAssignment", back_populates="room")
    tasks = relationship("Task", back_populates="room")


class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    type = Column(String(50))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Enum(ReservationStatus))
    payment_status = Column(Enum(PaymentStatus))
    total_cost = Column(Float)
    special_request = Column(String(200))
    
    client = relationship("Client", back_populates="reservations")


class RoomAssignment(Base):
    __tablename__ = "room_assignments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    rfid_code = Column(Integer, unique=True)
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    expense = Column(Float)
    
    client = relationship("Client", back_populates="room_assignments")
    room = relationship("Room", back_populates="room_assignments")


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    type = Column(Enum(DeviceType))
    value = Column(Integer)
    
    room = relationship("Room", back_populates="devices")


class ElectricityConsumption(Base):
    __tablename__ = "electricity_consumption"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_assignment_id = Column(Integer, ForeignKey("room_assignments.id"))
    timestamp = Column(DateTime)
    consumption = Column(Float)
    
    room_assignment = relationship("RoomAssignment")


class WaterConsumption(Base):
    __tablename__ = "water_consumption"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_assignment_id = Column(Integer, ForeignKey("room_assignments.id"))
    timestamp = Column(DateTime)
    consumption = Column(Float)
    
    room_assignment = relationship("RoomAssignment")


class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    role = Column(Enum(StaffRole))
    working = Column(Boolean)
    salary = Column(Float)
    phone_number = Column(String(50))
    email = Column(String(100))
    shift_schedule = Column(JSON)
    
    tasks = relationship("Task", back_populates="staff")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    task_status = Column(Enum(TaskStatus))
    assigned_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    staff = relationship("Staff", back_populates="tasks")
    room = relationship("Room", back_populates="tasks")
