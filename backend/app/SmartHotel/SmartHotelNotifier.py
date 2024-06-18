import paho.mqtt.client as mqtt
import json

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
        print(f"Hotel Notifier: Connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        print(f"Hotel Notifier: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, rc,  properties=None):
        print(f"Message published with ID: {mid}")

    def notify_event(self, event):
        payload = {"event": event}
        self.client.publish("hotel/events/notify", json.dumps(payload))
        print(f"Event notification sent: {event}")

    def notify_cleaning_staff(self, room_number):
        payload = {"room_number": room_number}
        self.client.publish("hotel/cleaning_staff/notify", json.dumps(payload))
        print(f"Cleaning staff notification sent for room {room_number}")
    
    def notify_smoke_alarm(self, room_number):
        payload = {"room_number": room_number}
        self.client.publish("hotel/security/notify", json.dumps(payload))
        print(f"Security notification sent for room {room_number}")