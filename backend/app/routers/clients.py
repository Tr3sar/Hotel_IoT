from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, storage as storage_module
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener la instancia global de storage
def get_storage():
    from app.main import storage
    return storage

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_client(db=db, client=client)

@router.get("/", response_model=List[schemas.Client])
def get_clients(skip: int = 0, limit: int = 10, storage: storage_module.Storage = Depends(get_storage)):
    clients = storage.get_clients(skip=skip, limit=limit)
    return clients

@router.put("/{client_id}/check_in")
def check_in(client_id: int, request: schemas.CheckInRequest, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.check_in(db=db, client_id=client_id, rfid_code=request.rfid_code, room_number=request.room_number)

@router.put("/{client_id}/check_out")
def check_out(client_id: int, request: schemas.CheckInRequest, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.check_out(db=db, client_id=client_id, rfid_code=request.rfid_code, room_number=request.room_number)
"""
@router.put("/{client_id}/adjust_environment")
def adjust_environment(client_id: int, request: schemas.AdjustEnvironmentRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.adjust_environment(client_id=client_id, temperature=request.temperature, lighting_intensity=request.lighting_intensity)
"""
@router.put("/{client_id}/request_cleaning")
def request_cleaning(client_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.request_cleaning(db=db, client_id=client_id)

@router.post("/{client_id}/order_restaurant")
def order_restaurant(client_id: int, request: schemas.OrderRestaurantRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.order_restaurant(client_id=client_id, order_details=request.order_details)
