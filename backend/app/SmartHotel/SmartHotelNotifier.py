import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('SmartHotel')

class SmartHotelNotifier:
    def __init__(self, hotel, broker, port):
        self.hotel = hotel
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hotel.notifier")
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
        logger.info(f"Hotel Notifier: Connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, extra, properties=None):
        logger.info(f"Hotel Notifier: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, rc,  properties=None):
        logger.info(f"Message published with ID: {mid}")

    def notify_event(self, event):
        payload = {"event": event}
        self.client.publish("hotel/events/info", json.dumps(payload))
        logger.info(f"Event notification sent: {event}")
    
    def notify_room_status(self, room_number, status):
        payload = {"room_number": room_number, "status": status}
        self.client.publish(f"hotel/rooms/{room_number}/status", json.dumps(payload))
        logger.info(f"Room {room_number}: {status}")

    def notify_clean_required(self, staff_id, room_number):
        payload = {"staff_id": staff_id, "room_number": room_number, "status": "CLEAN_REQUIRED"}
        logger.info(f"Room {room_number} assigned to staff {staff_id} for cleaning")
        self.client.publish(f"hotel/staff/cleanliness/{staff_id}/tasks", json.dumps(payload))

    def notify_smoke_alarm(self, room_number, staff_id, smoke_level):
        payload = {"room_number": room_number, "smoke_level": smoke_level}
        self.client.publish(f"hotel/staff/security/{staff_id}/alert", json.dumps(payload))
        logger.info(f"Security notification sent for room {room_number}")