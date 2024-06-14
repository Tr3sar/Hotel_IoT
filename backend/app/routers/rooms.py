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

@router.post("/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends()):
    db_room = storage.get_room_by_number(db, number=room.number)
    if db_room:
        raise HTTPException(status_code=400, detail="Room already registered")
    return storage.create_room(db=db, room=room)

@router.get("/{room_id}", response_model=schemas.Room)
def get_room(room_id: int, storage: storage_module.Storage = Depends()):
    room = storage.get_room(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/", response_model=List[schemas.Room])
def get_rooms(skip: int = 0, limit: int = 10, storage: storage_module.Storage = Depends()):
    rooms = storage.get_rooms(skip=skip, limit=limit)
    return rooms
