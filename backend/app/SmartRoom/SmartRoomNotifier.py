import paho.mqtt.client as mqtt
import json

class SmartRoomNotifier:
    def __init__(self, room, broker, port):
        self.smartRoom = room
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id=f"room{self.smartRoom.get_number()}.notifier")
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
        print(f"SmartRoom {self.smartRoom.get_number()}: Client connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, mid, rc, properties=None):
        print(f"SmartRoom {self.smartRoom.get_number()}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, rc, properties=None):
        print(f"Message published with ID: {mid}")

    def notify_room_status(self, room_number, status):
        payload = {"room_number": room_number, "status": status}
        self.client.publish(f"hotel/rooms/{room_number}/status", json.dumps(payload))
        print(f"Room status notification sent for room {room_number} with status {status}")
