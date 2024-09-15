from app.Staff.CleaningStaff.CleaningStaffSubscriber import CleaningStaffSubscriber
from app.Staff.CleaningStaff.CleaningStaffNotifier import CleaningStaffNotifier

import time
import threading

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CleaningStaff:
    def __init__(self, staff_id, name, working):
        self.staff_id = staff_id
        self.name = name
        self.role = "cleaning"
        self.working = working
        self.current_tasks = []
        self.notifier = CleaningStaffNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = CleaningStaffSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_id(self):
        return self.staff_id
    
    def get_tasks(self):
        return self.current_tasks

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

    def assign_task(self, room_number):
        self.current_tasks.append(room_number)
    
    def start_task(self, room_number):
        if self.current_tasks and room_number in self.current_tasks:
            self.notifier.notify_task_started(room_number)

    def complete_task(self, room_number):
        if self.current_tasks and room_number in self.current_tasks:

            self.notifier.notify_task_completed(room_number)
            self.current_tasks.remove(room_number)
            