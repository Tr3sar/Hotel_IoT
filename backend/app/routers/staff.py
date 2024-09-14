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

@router.post("/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_staff(db=db, staff=staff)

@router.get("/{staff_id}", response_model=schemas.Staff)
def get_staff(staff_id: int, storage: storage_module.Storage = Depends(get_db)):
    staff = storage.get_staff_by_id(staff_id)
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.get("/", response_model=List[schemas.Staff])
def get_staff(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    staff = storage.get_staff(db, skip=skip, limit=limit)
    return staff

@router.put("/{staff_id}/shift", response_model=schemas.Staff)
def update_shift_status(staff_id: int, request: schemas.StaffShiftRequest, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.update_shift_status(db=db, staff_id=staff_id, working=request.working)