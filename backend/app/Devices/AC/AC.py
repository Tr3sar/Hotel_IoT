from app.Devices.AC.ACSubscriber import ACSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class AC:
    def __init__(self, room_number):
        self.room_number = room_number
        self.temperature = 22
        self.subscriber = ACSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_room_number(self):
        return self.room_number

    def set_temperature(self, temperature):
        self.temperature = temperature