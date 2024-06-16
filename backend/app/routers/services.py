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

def get_storage():
    from app.main import storage
    return storage

@router.post("/reservation", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends()):
    return storage.create_reservation(db=db, reservation=reservation)

@router.get("/reservation", response_model=List[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 10, storage: storage_module.Storage = Depends()):
    reservations = storage.get_reservations(skip=skip, limit=limit)
    return reservations
