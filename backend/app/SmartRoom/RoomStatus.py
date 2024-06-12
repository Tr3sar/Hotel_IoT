from enum import Enum

class RoomStatus(Enum):
    CLEAN = 'clean'
    CLEAN_REQUIRED = 'clean-required'
    CLEANING = 'cleaning'
