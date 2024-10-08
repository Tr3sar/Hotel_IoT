import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('SmartClient')

class SmartClientSubscriber:
    def __init__(self, client, broker, port):
        self.smartClient = client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id=f"client{self.smartClient.getClientId()}.subscriber")
        self.broker = broker
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


        self.connect()
        self.client.loop_start()

    def _debug(self, message):
        logger.info(f"(SmartClient: {self.smartClient.getClientId()}) {message}")

    def loop_forever(self):
        self.client.loop_forever()
    
    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        logger.info(f"Connected to broker {self.broker} on port {self.port}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Connected to broker with result code {rc}")

        self.client.subscribe(f"hotel/events/info")

        #Al fer checkin es suscriu a hotel/rooms/{self.smartClient.getRoom()}/#

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        
        if msg.topic == "hotel/events/info":
            self.handle_events_info(data)
        elif msg.topic == f"hotel/rooms/{self.smartClient.getRoom()}/status":
            self.handle_room_status(data)     
        elif msg.topic == f"hotel/rooms/{self.smartClient.getRoom()}/consumption":
            self.handle_consumption(data)   

    def handle_events_info(self, data):
        event_info = data["event"]
        logger.info(f"Received event info: {event_info}")
    
    def handle_room_status(self, data):
        status = data["status"]
        #self._debug(f"Received room status: {data}")
    
    def handle_consumption(self, data):
        type = data["type"]

        if type == "electricity":
            current = data["current"]
            self.smartClient.addCurrent(current)
        elif type == "water":
            flow_rate = data["flow_rate"]
            self.smartClient.addFlowRate(flow_rate)