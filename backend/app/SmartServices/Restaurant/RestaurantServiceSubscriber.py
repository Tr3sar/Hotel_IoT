import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('SmartServices')

class RestaurantServiceSubscriber:
    def __init__(self,restaurant, broker, port):
        self.restaurant = restaurant
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="RestaurantService.subscriber")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc, properties = None):
        logger.info(f"Restaurant Service Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/clients/+/reservations")
        self.client.subscribe("hotel/clients/+/orders")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())

        if "reservations" in msg.topic:
            self.handle_reservation(data)
        elif "orders" in msg.topic:
            self.handle_order(data)

    def handle_reservation(self, data):
        type = data["type"]
        if type != "restaurant":
            return
        
        client_id = data["client_id"]
        start_date = data["start_date"]
        special_request = data["special_request"]
        
        logger.info(f"New restaurant reservation: Client {client_id} at {start_date} with special request: {special_request}")

        self.restaurant.make_reservation(client_id, start_date, special_request)
    
    def handle_order(self, data):
        client_id = data["client_id"]
        order_details = data["order_details"]

        logger.info(f"New restaurant order: Client {client_id} ordered {order_details}")