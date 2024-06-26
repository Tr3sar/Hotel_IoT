import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Sensors')

class SmokeSensorNotifier:
    def __init__(self, sensor, broker, port):
        self.sensor = sensor
        self.client = mqtt.Client(client_id=f"SmokeSensor-{self.sensor.get_sensor_id()}.notifier")
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

    def notify_smoke_detected(self, room_number, smoke_level):
        payload = {"room_number": room_number, "smoke_level": smoke_level}
        self.client.publish(f"hotel/rooms/{room_number}/fire", json.dumps(payload))
        logger.info(f"Smoke detected notification sent for room {room_number} with smoke level {smoke_level}")
