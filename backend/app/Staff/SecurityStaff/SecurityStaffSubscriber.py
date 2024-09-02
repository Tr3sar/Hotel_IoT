import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Staff')

class SecurityStaffSubscriber:
    def __init__(self, staff, broker, port):
        self.staff = staff
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"SecurityStaff-{self.staff.get_id()}.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"SecurityStaff Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe(f"hotel/staff/security/{self.staff.staff_id}/alert")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        if msg.topic == f"hotel/staff/security/{self.staff.staff_id}/alert":
            self.handle_alert(data)

    def handle_alert(self, data):
        room_number = data["room_number"]
        smoke_level = data["smoke_level"]
        self.staff.manage_fire_alarm(room_number)
        logger.info(f"Security alert for room {room_number} with smoke level {smoke_level} managed by staff {self.staff.staff_id}")