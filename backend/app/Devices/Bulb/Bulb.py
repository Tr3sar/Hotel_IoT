from app.Devices.Bulb.BulbSubscriber import BulbSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class Bulb:
    def __init__(self, room_number):
        self.room_number = room_number
        self.intensity = 100
        self.subscriber = BulbSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def get_room_number(self):
        return self.room_number

    def set_intensity(self, intensity):
        self.intensity = intensity