import paho.mqtt.client as mqtt
import json

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
        print(f"Hotel Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/rooms/+/status")
    
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())

        if "status" in msg.topic:
            self.handle_room_status(data)

    def handle_room_status(self, data):
        status = data["status"]
        room_number = data["room_number"]

        if status == "CLEAN_REQUIRED":
            self.hotel.notify_cleaning_staff(room_number)
