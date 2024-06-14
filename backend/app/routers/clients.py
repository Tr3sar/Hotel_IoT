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
