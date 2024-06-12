from app.SmartHotel.SmartHotelNotifier import SmartHotelNotifier
from app.SmartHotel.SmartHotelSubscriber import SmartHotelSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class SmartHotel:
    def __init__(self):

        self.notifier = SmartHotelNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = SmartHotelSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def notify_event(self, event):
        self.notifier.notify_event(event)
    
    def notify_cleaning_staff(self, room_number):
        self.notifier.notify_cleaning_staff(room_number)
    
    def notify_smoke_alarm(self, room_number):
        self.notifier.notify_smoke_alarm(room_number)