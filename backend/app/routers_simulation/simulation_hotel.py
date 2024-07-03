from fastapi import APIRouter, Depends
from app import schemas, storage as storage_module

router = APIRouter()


def get_storage():
    from app.main import storage
    return storage

@router.post("/event")
def notify_event(event: schemas.EventNotification, storage: storage_module.Storage = Depends(get_storage)):
    storage.notify_event(event_info=event.info)
    return {"message": "Event notification sent successfully"}
