import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Staff')

class CleaningStaffNotifier:
    def __init__(self, staff, broker, port):
        self.staff = staff
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"CleaningStaff-{self.staff.get_id()}.notifier")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"CleaningStaff {self.staff.staff_id}: Connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        logger.info(f"CleaningStaff {self.staff.staff_id}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, properties=None):
        logger.info(f"Message published with ID: {mid}")

    def notify_shift_start(self):
        payload = {"staff_id": self.staff.staff_id, "status": "start"}
        self.client.publish(f"hotel/staff/cleanliness/{self.staff.staff_id}/shift", json.dumps(payload))
        logger.info(f"Shift start notification sent for staff {self.staff.staff_id}")

    def notify_shift_end(self):
        payload = {"staff_id": self.staff.staff_id, "status": "end"}
        self.client.publish(f"hotel/staff/cleanliness/{self.staff.staff_id}/shift", json.dumps(payload))
        logger.info(f"Shift end notification sent for staff {self.staff.staff_id}")

    def notify_task_completed(self, room_number):
        payload = {"staff_id": self.staff.staff_id, "room_number": room_number, "status": "completed"}
        self.client.publish(f"hotel/staff/cleanliness/{self.staff.staff_id}/tasks", json.dumps(payload))
        logger.info(f"Task completed notification sent for room {room_number}")