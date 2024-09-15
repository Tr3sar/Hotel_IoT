import paho.mqtt.client as mqtt
import json

from app.schemas import RoomStatus

import logging
logger = logging.getLogger('SmartClient')

class SmartClientNotifier:
    def __init__(self, client, broker, port):
        self.smartClient = client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id=f"client{self.smartClient.getClientId()}.notifier")
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
        logger.info(f"SmartClient {self.smartClient.getClientId()}: Client connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, mid, rc, properties=None):
        logger.info(f"SmartClient {self.smartClient.getClientId()}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, rc, properties=None):
        logger.info(f"Message published with ID: {mid}")

    def notify_checkin(self, client_id, rfid_code, room_number):
        payload = {"client_id": client_id, "rfid_code": rfid_code, "room_number": room_number}
        self.client.publish(f"hotel/rooms/{room_number}/checkin", json.dumps(payload))
        logger.info(f"Check-in notification sent for client: {client_id} with RFID {rfid_code} in room {room_number}")

    def notify_checkout(self, client_id, room_number):
        payload = {"client_id": client_id, "room_number": room_number}
        self.client.publish(f"hotel/rooms/{room_number}/checkout", json.dumps(payload))
        logger.info(f"Check-out notification sent for client: {client_id} from room {room_number}")

    def notify_adjust_environment(self, room_number, temperature, lightning_intensity):
        payload = {"room_number": room_number, "temperature": temperature, "lightning_intensity": lightning_intensity}
        self.client.publish(f"hotel/rooms/{room_number}/environment", json.dumps(payload))
        logger.info(f"Environment adjustment notification sent for room {room_number} with temperature {temperature} and lightning intensity {lightning_intensity}")

    def notify_cleaning_request(self, room_number, room_id):
        payload = {"room_number": room_number, "status": RoomStatus.CLEAN_REQUIRED.value, "room_id": room_id}
        self.client.publish(f"hotel/rooms/{room_number}/status", json.dumps(payload))
        logger.info(f"Cleaning request notification sent for room {room_number}")
        
    def notify_reservation(self, client_id, type, start_date):
        payload = {"client_id": client_id, "type": type, "start_date": start_date.isoformat()}
        self.client.publish(f"hotel/clients/{client_id}/reservations", json.dumps(payload))
        logger.info(f"Reservation notification sent for client: {client_id} for the service: {type} at {start_date}")

    def notify_order(self, client_id, order_details):
        payload = {"client_id": client_id, "order_details": order_details}
        self.client.publish(f"hotel/clients/{client_id}/orders", json.dumps(payload))
        logger.info(f"Order notification sent for client: {client_id} with details: {order_details}")

    
