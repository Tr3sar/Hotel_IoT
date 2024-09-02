from fastapi import APIRouter, Depends, HTTPException
from app import storage as storage_module

router = APIRouter()

def get_storage():
    from app.main import storage
    return storage

@router.put("/{staff_id}/start-shift")
def start_shift(staff_id: int, storage: storage_module.Storage = Depends(get_storage)):
    try:
        cleaning_staff = storage.start_shift(staff_id=staff_id)
        return cleaning_staff
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{staff_id}/end-shift")
def end_shift(staff_id: int, storage: storage_module.Storage = Depends(get_storage)):
    try:
        cleaning_staff = storage.end_shift(staff_id=staff_id)
        return cleaning_staff
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/cleaning/{staff_id}/complete-task")
def complete_task(staff_id: int, storage: storage_module.Storage = Depends(get_storage)):
    try:
        cleaning_staff = storage.complete_task(staff_id=staff_id)
        return cleaning_staff
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
