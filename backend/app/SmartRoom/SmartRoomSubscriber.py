import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('SmartRoom')

class SmartRoomSubscriber:
    def __init__(self, room, broker, port):
        self.smartRoom = room
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id=f"room{self.smartRoom.get_number()}.subscriber")
        self.broker = broker
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


        self.connect()
        self.client.loop_start()

    def _debug(self, message):
        logger.info(f"(SmartRoom: {self.smartRoom.get_number()}) {message}")

    def loop_forever(self):
        self.client.loop_forever()
    
    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        logger.info(f"Connected to broker {self.broker} on port {self.port}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Connected to broker with result code {rc}")

        self.client.subscribe(f"hotel/rooms/{self.smartRoom.get_number()}/checkin")
        self.client.subscribe(f"hotel/rooms/{self.smartRoom.get_number()}/checkout")
        self.client.subscribe(f"hotel/rooms/{self.smartRoom.get_number()}/environment")
        self.client.subscribe(f"hotel/rooms/{self.smartRoom.get_number()}/status")



    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        
        if msg.topic.endswith("checkin"):
            self.handle_checkin(data)
        elif msg.topic.endswith("checkout"):
            self.handle_checkout(data)
        elif msg.topic.endswith("status"):
            self.handle_room_status(data)
        elif msg.topic.endswith("environment"):
            self.handle_adjust_environment(data)


    def handle_checkin(self, data):
        client_id = data["client_id"]
        rfid_code = data["rfid_code"]

        logger.info(f"Client {client_id} checked in")
        self.smartRoom.occupy(client_id, rfid_code)

    def handle_checkout(self, data):
        client_id = data["client_id"]

        logger.info(f"Client {client_id} checked out")
        self.smartRoom.vacate(client_id)
    
    def handle_room_status(self, data):
        status = data["status"]
        logger.info(f"New status: {status}")
        self.smartRoom.setRoomStatus(status)

    
    def handle_adjust_environment(self, data):
        temperature = data["temperature"]
        lightning_intensity = data["lightning_intensity"]

        logger.info(f"Adjusting environment to Temp={temperature}, LI={lightning_intensity}")
        self.smartRoom.adjust_environment(temperature, lightning_intensity)
    
    #TODO: L'habitació deuria rebre les dades de consum? (Ja les rep el client)
    def handle_light_consumption(self, data):
        logger.info(f"Room {self.smartRoom.get_number()} consumed {data['light_consumption']}W of light")
    
    def handle_water_consumption(self, data):
        logger.info(f"Room {self.smartRoom.get_number()} consumed {data['water_consumption']}L of water")
