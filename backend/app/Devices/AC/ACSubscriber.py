import paho.mqtt.client as mqtt
import json

class ACSubscriber:
    def __init__(self, ac, broker, port):
        self.ac = ac
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"AC-{self.ac.get_room_number()}.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"AC Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe(f"hotel/rooms/{self.ac.get_room_number()}/ac/temperature")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_temperature_change(data)

    def handle_temperature_change(self, data):
        room_number = data["room_number"]
        temperature = data["temperature"]
        self.ac.set_temperature(temperature)
        print(f"Temperature change for room {room_number}: {temperature}")