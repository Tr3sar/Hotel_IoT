import paho.mqtt.client as mqtt
import json

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
        print(f"(SmartRoom: {self.smartRoom.get_number()}) {message}")

    def loop_forever(self):
        self.client.loop_forever()
    
    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        print(f"Connected to broker {self.broker} on port {self.port}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Connected to broker with result code {rc}")

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
        elif msg.topic.endswith("adjust_environment"):
            self.handle_adjust_environment(data)
        elif msg.topic.endswith("light_consumption"):
            self.handle_light_consumption(data)
        elif msg.topic.endswith("water_consumption"):
            self.handle_water_consumption(data)


    def handle_checkin(self, data):
        client_id = data["client_id"]

        self._debug(f"Client {client_id} checked in")
        self.smartRoom.occupy(client_id)

    def handle_checkout(self, data):
        client_id = data["client_id"]

        self._debug(f"Client {client_id} checked out")
        self.smartRoom.vacate(client_id)
    
    def handle_room_status(self, data):
        status = data["status"]
        print(f"New status: {status}")
        self.smartRoom.setRoomStatus(status)

    
    def handle_adjust_environment(self, data):
        temperature = data["temperature"]
        lightning_intensity = data["lightning_intensity"]

        self._debug(f"Adjusting environment to Temp={temperature}, LI={lightning_intensity}")
        self.smartRoom.adjust_environment(temperature, lightning_intensity)
    
    #TODO: Implement light and water consumption handling and sensors
    def handle_light_consumption(self, data):
        print(f"Room {self.smartRoom.get_number()} consumed {data['light_consumption']}W of light")
    
    def handle_water_consumption(self, data):
        print(f"Room {self.smartRoom.get_number()} consumed {data['water_consumption']}L of water")
