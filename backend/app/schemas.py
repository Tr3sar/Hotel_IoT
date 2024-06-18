from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class RoomBase(BaseModel):
    number: int
    status: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    name: str
    email: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    reservations: List["Reservation"] = []

    class Config:
        from_attributes = True

class CleaningStaffBase(BaseModel):
    name: str

class CleaningStaffCreate(CleaningStaffBase):
    pass

class CleaningStaff(CleaningStaffBase):
    id: int

    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    client_id: int
    reservation_type: str
    start_date: datetime

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    client: Client

    class Config:
        from_attributes = True

class RoomAssignmentBase(BaseModel):
    client_id: int
    room_id: int
    rfid_code: int

class RoomAssignmentCreate(RoomAssignmentBase):
    pass

class RoomAssignment(RoomAssignmentBase):
    id: int

    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    room_id: int
    type: str
    value: int

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int

    class Config:
        from_attributes = True

class CheckInRequest(BaseModel):
    rfid_code: int
    room_number: int

class AdjustEnvironmentRequest(BaseModel):
    temperature: int
    lighting_intensity: int

class CleaningRequest(BaseModel):
    client_id: int

class ReserveServiceRequest(BaseModel):
    reservation_type: str
    time: str

class OrderRestaurantRequest(BaseModel):
    order_details: str

class UpdateRoomStatusRequest(BaseModel):
    status: str
