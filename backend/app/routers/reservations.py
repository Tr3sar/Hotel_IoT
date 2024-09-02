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

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_reservation(db=db, reservation=reservation)

@router.get("/", response_model=List[schemas.Reservation])
def get_reservations(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.get_reservations(db=db, skip=skip, limit=limit)

@router.get("/{reservation_id}", response_model=schemas.Reservation)
def get_reservation(reservation_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    reservation = storage.get_reservation(db=db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
