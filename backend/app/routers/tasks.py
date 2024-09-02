from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, storage as storage_module
from app.database import SessionLocal

router = APIRouter()

# Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_storage():
    from app.main import storage
    return storage

# Rutas

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_task(db=db, task=task)

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    task = storage.get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=List[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    tasks = storage.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.Task, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    updated_task = storage.update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    deleted_task = storage.delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task

@router.get("/staff/{staff_id}", response_model=List[schemas.Task])
def get_tasks_by_staff_id(staff_id: int, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    tasks = storage.get_tasks_by_staff_id(db, staff_id=staff_id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="No tasks found for the given staff ID")
    return tasks