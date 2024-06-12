import paho.mqtt.client as mqtt
import json

class SpaServiceSubscriber:
    def __init__(self, spa, broker, port):
        self.spa = spa
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="SpaService.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Spa Service Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/spa/appointments")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_appointment(data)

    def handle_appointment(self, data):
        client_id = data["client_id"]
        time = data["time"]
        self.spa.book_appointment(client_id, time)
        print(f"New appointment: Client {client_id} at {time}")