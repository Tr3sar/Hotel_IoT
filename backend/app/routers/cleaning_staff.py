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

@router.post("/", response_model=schemas.CleaningStaff)
def create_cleaning_staff(staff: schemas.CleaningStaffCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_cleaning_staff(db=db, staff=staff)

@router.get("/{staff_id}", response_model=schemas.CleaningStaff)
def get_cleaning_staff(staff_id: int, storage: storage_module.Storage = Depends(get_db)):
    staff = storage.get_cleaning_staff_by_id(staff_id)
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.get("/", response_model=List[schemas.CleaningStaff])
def get_cleaning_staff(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    staff = storage.get_cleaning_staff(db, skip=skip, limit=limit)
    return staff

@router.put("/{staff_id}", response_model=schemas.CleaningStaff)
def update_cleaning_staff(staff_id: int, staff: schemas.CleaningStaff, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.update_cleaning_staff(db=db, staff_id=staff_id, staff=staff)
