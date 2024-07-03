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

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Spa Service Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/clients/+/reservations")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_reservation(data)

    def handle_reservation(self, data):
        reservation_type = data["reservation_type"]
        if reservation_type != "spa":
            return
        
        client_id = data["client_id"]
        start_date = data["start_date"]
        #Fer la reserva també a través de mqtt? A part de la bd? En cas que si, tornar a posar l'atribut reservation_id
        logger.info(f"New reservation: Client {client_id} at {start_date}")