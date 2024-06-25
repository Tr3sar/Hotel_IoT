from app.Staff.CleaningStaff.CleaningStaffSubscriber import CleaningStaffSubscriber
from app.Staff.CleaningStaff.CleaningStaffNotifier import CleaningStaffNotifier

import time
import threading

import os
from dotenv import load_dotenv

load_dotenv()

class CleaningStaff:
    def __init__(self, staff_id, name, working):
        self.staff_id = staff_id
        self.name = name
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

    def end_shift(self):
        #Decidir que fer si encara hi ha tasques pendents de completar
        self.working = False
        self.notifier.notify_shift('end')

    def assign_task(self, room_number):
        if self.working:
            self.current_tasks.append(room_number)
        else:
            print(f"Staff {self.staff_id} is not working currently.")

    def complete_task(self):
        if self.current_tasks:
            room_number = self.current_tasks.pop(0)
            self.notifier.notify_task_started(room_number)
            
            def finish_cleaning():
                time.sleep(5)
                self.notifier.notify_task_completed(room_number)
            
            threading.Thread(target=finish_cleaning).start()