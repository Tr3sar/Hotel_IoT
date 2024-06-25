from app.SmartHotel.SmartHotelNotifier import SmartHotelNotifier
from app.SmartHotel.SmartHotelSubscriber import SmartHotelSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class SmartHotel:
    def __init__(self):
        self.cleaning_staff = {}
        self.active_cleaning_staff = set()

        self.notifier = SmartHotelNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = SmartHotelSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_active_cleaning_staff(self):
        return self.active_cleaning_staff

    def add_active_cleaning_staff(self, staff_id):
        self.active_cleaning_staff.add(staff_id)
        if staff_id not in self.cleaning_staff:
            self.cleaning_staff[staff_id] = {'tasks': 0}
    
    def remove_active_cleaning_staff(self, staff_id):
        self.active_cleaning_staff.discard(staff_id)
    
    def notify_event(self, event):
        self.notifier.notify_event(event)
    
    def notify_clean_required(self, room_number):
        assigned_staff = min(self.active_cleaning_staff, key=lambda staff_id: self.cleaning_staff[staff_id]['tasks'])
        self.cleaning_staff[assigned_staff]['tasks'] += 1

        self.notifier.notify_clean_required(assigned_staff, room_number) 
    
    def notify_room_cleaned(self, staff_id, room_number):
        self.cleaning_staff[staff_id]['tasks'] -= 1
        self.notifier.notify_room_status(room_number, 'clean')
    
    def notify_room_cleaning(self, room_number):
        self.notifier.notify_room_status(room_number, 'cleaning')
    
    #TODO: fa falta? A qui li avisa?
    def notify_smoke_alarm(self, room_number):
        self.notifier.notify_smoke_alarm(room_number)