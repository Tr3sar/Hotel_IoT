import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Services')

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
        logger.info(f"Spa Service Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/clients/+/reservations")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_appointment(data)

    def handle_appointment(self, data):
        client_id = data["client_id"]
        time = data["time"]
        self.spa.book_appointment(client_id, time)
        logger.info(f"New appointment: Client {client_id} at {time}")