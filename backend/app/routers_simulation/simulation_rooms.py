from fastapi import APIRouter, Depends, HTTPException
from app import schemas, storage as storage_module

router = APIRouter()

def get_storage():
    from app.main import storage
    return storage

@router.put("/{room_number}/status", response_model=schemas.Room)
def update_room_status(room_number: int, request: schemas.UpdateRoomStatusRequest, storage: storage_module.Storage = Depends(get_storage)):
    return storage.update_room_status(room_number=room_number, status=request.status)

@router.put("/{room_number}/environment", response_model=dict)
def adjust_environment(room_number: int, request: schemas.AdjustEnvironmentRequest, storage: storage_module.Storage = Depends(get_storage)):
    res = storage.adjust_environment(room_number=room_number, temperature=request.temperature, lighting_intensity=request.lighting_intensity)
    return res

@router.put("/{room_id}/simulate-fire")
def simulate_fire(room_id: int, storage: storage_module.Storage = Depends(get_storage)):
    try:
        storage.trigger_smoke_detection(room_id)
        return {"message": f"Simulated fire in room {room_id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))