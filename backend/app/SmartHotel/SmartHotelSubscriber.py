import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('SmartHotel')

class SmartHotelSubscriber:
    def __init__(self, hotel, broker, port):
        self.hotel = hotel
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hotel.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Hotel Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/rooms/+/status")
        self.client.subscribe("hotel/rooms/+/fire")
        self.client.subscribe("hotel/staff/cleanliness/+/tasks")
        self.client.subscribe("hotel/staff/+/shift")
    
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())

        if "status" in msg.topic:
            self.handle_cleaning_task(data, "status")
        elif "tasks" in msg.topic:
            self.handle_cleaning_task(data, "tasks")
        elif "shift" in msg.topic:
            self.handle_shift(data)
        elif "fire" in msg.topic:
            self.handle_fire_alarm(data)
    
    def handle_cleaning_task(self, data, topic):
        room_number = data["room_number"]
        status = data["status"]

        if topic == "status":
            if status == "clean-required":
                if not self.hotel.get_active_cleaning_staff():
                    logger.warning("No cleaning staff available")
                    return
                self.hotel.notify_clean_required(room_number)
                logger.info(f"Room {room_number} requires cleaning")
        elif topic == "tasks":
            if status == "clean":
                staff_id = data["staff_id"]
                self.hotel.notify_room_cleaned(staff_id, room_number)
            elif status == "cleaning":
                self.hotel.notify_room_cleaning(room_number)
    
    def handle_shift(self, data):
        status = data["status"]
        staff_id = data["staff_id"]
        role = data["role"]

        if status == 'start':
            self.hotel.add_active_staff(staff_id, role)
        elif status == 'end':
            self.hotel.remove_active_staff(staff_id, role)

    def handle_fire_alarm(self, data):
        room_number = data["room_number"]
        smoke_level = data["smoke_level"]

        self.hotel.notify_smoke_alarm(room_number, smoke_level)
        
        logger.info(f"Fire alarm notification sent for room {room_number} with smoke level {smoke_level}")