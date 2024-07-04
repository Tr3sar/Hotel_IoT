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

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    return storage.create_client(db=db, client=client)

@router.get("/", response_model=List[schemas.Client])
def get_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), storage: storage_module.Storage = Depends(get_storage)):
    clients = storage.get_clients(db, skip=skip, limit=limit)
    return clients

@router.get("/{client_id}", response_model=schemas.Client)
def get_client(client_id: int, storage: storage_module.Storage = Depends(get_storage)):
    client = storage.get_client(client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, storage: storage_module.Storage = Depends(get_storage)):
    updated_client = storage.update_client(client_id=client_id, client=client)
    if updated_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client
