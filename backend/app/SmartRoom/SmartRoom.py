from app.SmartRoom.SmartRoomNotifier import SmartRoomNotifier
from app.SmartRoom.SmartRoomSubscriber import SmartRoomSubscriber

from app.SmartRoom.RoomStatus import RoomStatus

import os
from dotenv import load_dotenv
load_dotenv()

class SmartRoom():
    def __init__(self, number):
        self.number = number
        self.temperature = 22
        self.lightning_intensity = 100
        self.occupied_by = None
        self.status = RoomStatus.CLEAN.value

        self.notifier = SmartRoomNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = SmartRoomSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_number(self):
        return self.number

    def adjust_environment(self, temperature, lightning_intensity):
        self.temperature = temperature
        self.lightning_intensity = lightning_intensity
        print(f"Room {self.number}: Temp={self.temperature}, LI={self.lightning_intensity}")

    def occupy(self, client_id):
        self.occupied_by = client_id
        print(f"Room {self.number} occupied by {self.occupied_by}")

    def vacate(self, client_id):
        if self.occupied_by == client_id:
            print(f"Room {self.number} vacated by {self.occupied_by}")
            self.occupied_by = None
    
    def setRoomStatus(self, status):
        if status in [status.value for status in RoomStatus]:
            self.status = status
            print(f"Room {self.number} status set to {status}")
        else:
            print("Invalid room status")
            
    def notifyRoomStatus(self, status):
        if status in [status.value for status in RoomStatus]:
            self.status = status
            self.notifier.notify_room_status(self.number, status)
            print(f"Room {self.number} status set to {status}")
        else:
            print("Invalid room status")