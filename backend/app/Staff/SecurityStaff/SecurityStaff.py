from app.Staff.SecurityStaff.SecurityStaffSubscriber import SecurityStaffSubscriber
from app.Staff.StaffNotifier import StaffNotifier

import time
import threading

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SecurityStaff:
    def __init__(self, staff_id, name, working):
        self.staff_id = staff_id
        self.name = name
        self.role = "security"
        self.working = working
        self.subscriber = SecurityStaffSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.notifier = StaffNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_id(self):
        return self.staff_id

    def manage_fire_alarm(self, room_number):
        if self.working:
            print(f"Staff {self.staff_id} is managing the fire alarm in room {room_number}")
        else:
            print(f"Staff {self.staff_id} is not working currently.")

    def start_shift(self):
        self.working = True
        self.notifier.notify_shift('start')
        url = os.getenv("API_URL") + f"/staff/{self.staff_id}/shift"
        put_payload = {"id":self.staff_id, "name":self.name, "working":self.working}
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "es",
        }
        response = requests.put(url, headers=headers, json=put_payload)

    def end_shift(self):
        self.working = False
        self.notifier.notify_shift('end')   

        url = os.getenv("API_URL") + f"/staff/{self.staff_id}/shift"
        put_payload = {"id": self.staff_id, "name":self.name, "working":self.working}
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "es",
        }
        response = requests.put(url, headers=headers, json=put_payload)