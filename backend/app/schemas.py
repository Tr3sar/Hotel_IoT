from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import List, Optional
from enum import Enum

class IDDocumentType(str, Enum):
    passport = 'passport'
    driver_license = 'driver_license'
    national_id = 'national_id'

class RoomType(str, Enum):
    single = 'single'
    double = 'double'
    suite = 'suite'

class RoomStatus(str, Enum):
    CLEAN = 'CLEAN'
    CLEANING = 'CLEANING'
    CLEAN_REQUIRED = 'CLEAN_REQUIRED'

class ReservationStatus(str, Enum):
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    in_process = 'in_process'

class PaymentStatus(str, Enum):
    pending = 'pending'
    paid = 'paid'

class DeviceType(str, Enum):
    AC = 'AC'
    Bulb = 'Bulb'

class StaffRole(str, Enum):
    cleaning = 'cleaning'
    security = 'security'
    maintenance = 'maintenance'

class TaskStatus(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    date_of_birth: date
    id_document_type: IDDocumentType
    id_document_number: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    number: int
    type: RoomType
    status: RoomStatus
    price: float
    floor: int
    description: Optional[str] = None
    max_occupancy: int
    last_maintenance: Optional[date] = None

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    devices: List['Device'] = []

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    client_id: int
    type: str
    start_date: datetime
    end_date: datetime
    status: ReservationStatus
    payment_status: PaymentStatus
    total_cost: float
    special_request: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int

    class Config:
        orm_mode = True


class RoomAssignmentBase(BaseModel):
    client_id: int
    room_id: int
    rfid_code: int
    check_in_date: datetime
    check_out_date: Optional[datetime] = None
    expense: float

class RoomAssignmentCreate(RoomAssignmentBase):
    pass

class RoomAssignment(RoomAssignmentBase):
    id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    type: DeviceType
    value: int

class DeviceCreate(DeviceBase):
    room_id: int

class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True


class ElectricityConsumptionBase(BaseModel):
    timestamp: datetime
    consumption: float

class ElectricityConsumptionCreate(ElectricityConsumptionBase):
    room_assignment_id: int

class ElectricityConsumption(ElectricityConsumptionBase):
    id: int
    room_assignment: RoomAssignment

    class Config:
        orm_mode = True


class WaterConsumptionBase(BaseModel):
    timestamp: datetime
    consumption: float

class WaterConsumptionCreate(WaterConsumptionBase):
    room_assignment_id: int

class WaterConsumption(WaterConsumptionBase):
    id: int
    room_assignment: RoomAssignment

    class Config:
        orm_mode = True


class StaffBase(BaseModel):
    name: str
    role: StaffRole
    working: bool
    salary: float
    phone_number: str
    email: str
    shift_schedule: dict

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: int
    tasks: List['Task'] = []

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    task_status: TaskStatus
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    staff_id: int
    room_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    room: Room

    class Config:
        orm_mode = True


class CheckInRequest(BaseModel):
    rfid_code: int
    room_number: int

class StaffShiftRequest(BaseModel):
    working: bool

class AdjustEnvironmentRequest(BaseModel):
    temperature: int
    lighting_intensity: int

class CleaningRequest(BaseModel):
    client_id: int

class ReserveServiceRequest(BaseModel):
    type: str
    time: str

class OrderRestaurantRequest(BaseModel):
    order_details: str

class UpdateRoomStatusRequest(BaseModel):
    status: str

class EventNotification(BaseModel):
    info: str