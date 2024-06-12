from app.Staff.CleaningStaff.CleaningStaffSubscriber import CleaningStaffSubscriber
from app.Staff.CleaningStaff.CleaningStaffNotifier import CleaningStaffNotifier
import os
from dotenv import load_dotenv

load_dotenv()

class CleaningStaff:
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name
        self.current_tasks = []
        self.working = False
        self.notifier = CleaningStaffNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = CleaningStaffSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_id(self):
        return self.staff_id

    def start_shift(self):
        self.working = True
        self.notifier.notify_shift_start()

    def end_shift(self):
        self.working = False
        self.notifier.notify_shift_end()

    def assign_task(self, room_number):
        if self.working:
            self.current_tasks.append(room_number)
            self.notifier.notify_task_assigned(room_number)
        else:
            print(f"Staff {self.staff_id} is not working currently.")

    def complete_task(self, room_number):
        if room_number in self.current_tasks:
            self.current_tasks.remove(room_number)
            self.notifier.notify_task_completed(room_number)