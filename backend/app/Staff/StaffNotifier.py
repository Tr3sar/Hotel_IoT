import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Staff')

class StaffNotifier:
    def __init__(self, staff, broker, port):
        self.staff = staff
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"Staff-{self.staff.get_id()}.notifier")
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
        logger.info(f"Staff {self.staff.staff_id}: Connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        logger.info(f"Staff {self.staff.staff_id}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, rc, properties=None):
        logger.info(f"Message published with ID: {mid}")

    def notify_shift(self, status):
        payload = {"staff_id": self.staff.staff_id, "status": status, "role": self.staff.role}
        self.client.publish(f"hotel/staff/{self.staff.staff_id}/shift", json.dumps(payload))
        logger.info(f"Shift {status} notification sent for staff {self.staff.staff_id}")