import paho.mqtt.client as mqtt
import json

class BulbSubscriber:
    def __init__(self, bulb, broker, port):
        self.bulb = bulb
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"Bulb-{self.bulb.get_room_number}.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Bulb Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe(f"hotel/rooms/{self.bulb.get_room_number()}/bulb/intensity")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_intensity_change(data)

    def handle_intensity_change(self, data):
        room_number = data["room_number"]
        intensity = data["intensity"]
        self.bulb.set_intensity(intensity)
        print(f"Intensity change for room {room_number}: {intensity}")