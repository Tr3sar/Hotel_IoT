import paho.mqtt.client as mqtt
import json

from app.Staff.StaffNotifier import StaffNotifier

import logging
logger = logging.getLogger('Staff')

class CleaningStaffNotifier(StaffNotifier):
    def notify_task_started(self, room_number):
        payload = json.dumps({"room_number": room_number, "status": "CLEANING"})
        self.client.publish(f"hotel/staff/cleanliness/{self.staff.staff_id}/tasks", payload)
        logger.info(f"Notified start of cleaning for room {room_number}")

    def notify_task_completed(self, room_number):
        payload = {"staff_id": self.staff.staff_id, "room_number": room_number, "status": "CLEAN"}
        self.client.publish(f"hotel/staff/cleanliness/{self.staff.staff_id}/tasks", json.dumps(payload))
        logger.info(f"Task completed notification sent for room {room_number}")