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

@router.post("/", response_model=schemas.RoomAssignment)
def create_room_assignment(room_assignment: schemas.RoomAssignmentCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_room_assignment(db=db, assignment=room_assignment)

@router.get("/", response_model=List[schemas.RoomAssignment])
def get_room_assignments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    room_assignments = storage.get_room_assignments(db, skip=skip, limit=limit)
    return room_assignments

@router.get("/{room_assignment_id}", response_model=schemas.RoomAssignment)
def get_room_assignment(room_assignment_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    room_assignment = storage.get_room_assignment(db, room_assignment_id=room_assignment_id)
    if room_assignment is None:
        raise HTTPException(status_code=404, detail="Room assignment not found")
    return room_assignment

@router.delete("/{room_assignment_id}", response_model=schemas.RoomAssignment)
def delete_room_assignment(room_assignment_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    room_assignment = storage.delete_room_assignment(db, room_assignment_id=room_assignment_id)
    if room_assignment is None:
        raise HTTPException(status_code=404, detail="Room assignment not found")
    return room_assignment