import paho.mqtt.client as mqtt
import json

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
        print(f"Restaurant Service Subscriber: Connected to broker with result code {rc}")
        self.client.subscribe("hotel/restaurant/reservations")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        self.handle_reservation(data)

    def handle_reservation(self, data):
        client_id = data["client_id"]
        time = data["time"]
        self.restaurant.make_reservation(client_id, time)
        print(f"New reservation: Client {client_id} at {time}")