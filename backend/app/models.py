from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    status = Column(String(50), default="clean")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)

class CleaningStaff(Base):
    __tablename__ = "cleaning_staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    working = Column(Boolean, default=False)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    reservation_type = Column(String(50))
    start_date = Column(DateTime)
    client = relationship("Client", back_populates="reservations")

    __table_args__ = (UniqueConstraint('client_id', 'start_date', name='unique_client_start_date'),)

class RoomAssignment(Base):
    __tablename__ = "room_assignments"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    rfid_code = Column(Integer, unique=True, nullable=False)

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    type = Column(String(50))
    value = Column(Integer)
    room = relationship("Room", back_populates="devices")

    def __init__(self, **kwargs):
        super(Device, self).__init__(**kwargs)
        if self.type == "AC":
            self.value = 22
        elif self.type == "Light":
            self.value = 100

Room.devices = relationship("Device", order_by=Device.id, back_populates="room")
Client.reservations = relationship("Reservation", order_by=Reservation.id, back_populates="client")

class ElectricityConsumption(Base):
    __tablename__ = "electricity_consumption"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    timestamp = Column(DateTime)
    consumption = Column(Float)

class WaterConsumption(Base):
    __tablename__ = "water_consumption"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    timestamp = Column(DateTime)
    consumption = Column(Float)

"""
@event.listens_for(Device, 'init')
def receive_init(target, args, kwargs):
    if target.type == "AC":
        target.value = 22
    elif target.type == "Light":
        target.value = 100
"""