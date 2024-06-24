import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Staff')

class CleaningStaffSubscriber:
    def __init__(self, staff, broker, port):
        self.staff = staff
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"CleaningStaff-{self.staff.get_id()}.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"CleaningStaff Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe(f"hotel/staff/cleanliness/{self.staff.get_id()}/task")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        if msg.topic == f"hotel/staff/cleanliness/{self.staff.get_id()}/task":
            self.handle_task(data)

    def handle_task(self, data):
        staff_id = data["staff_id"]
        room_number = data["room_number"]
        status = data["status"]
        self.staff.add_task(room_number, status)
        logger.info(f"Task update for staff {staff_id} on room {room_number}: {status}")