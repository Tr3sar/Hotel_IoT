import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Sensors')

class ElectricityConsumptionSensorNotifier:
    def __init__(self, sensor, broker, port):
        self.sensor = sensor
        self.client = mqtt.Client(client_id=f"ElectricityConsumptionSensor-{self.sensor.get_sensor_id()}.notifier")
        self.broker = broker
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

        self.connect()
        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Sensor {self.sensor.get_sensor_id()}: Client connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        logger.info(f"Sensor {self.sensor.get_sensor_id()}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, properties=None):
        logger.info(f"Message published with ID: {mid}")

    def notify_current(self, room_id, current):
        payload = {"room_id": room_id, "type": "electricity", "current": current}
        self.client.publish(f"hotel/rooms/{room_id}/consumption", json.dumps(payload))
        logger.info(f"Current notification sent for room {room_id} with current {current}")
