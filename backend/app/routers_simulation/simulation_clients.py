from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import schemas, storage as storage_module

router = APIRouter()

def get_storage():
    from app.main import storage
    return storage

@router.put("/{client_id}/check_in")
def check_in(client_id: int, request: schemas.CheckInRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.check_in(client_id=client_id, rfid_code=request.rfid_code, room_number=request.room_number)

@router.put("/{client_id}/check_out")
def check_out(client_id: int, request: schemas.CheckInRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.check_out(client_id=client_id, rfid_code=request.rfid_code, room_number=request.room_number)

@router.put("/{client_id}/request_cleaning")
def request_cleaning(client_id: int, storage: storage_module.Storage = Depends(get_storage)):
    return storage.request_cleaning(client_id=client_id)

@router.put("/{client_id}/reservation")
def reservation(client_id: int, reservation: schemas.ReservationCreate, storage: storage_module.Storage = Depends(get_storage)):
    return storage.make_reservation(client_id, reservation=reservation)

@router.post("/{client_id}/order_restaurant")
def order_restaurant(client_id: int, request: schemas.OrderRestaurantRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.order_restaurant(client_id=client_id, order_details=request.order_details)
