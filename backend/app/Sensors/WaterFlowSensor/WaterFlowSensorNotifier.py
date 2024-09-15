import paho.mqtt.client as mqtt
import json

import logging
logger = logging.getLogger('Sensors')

class WaterFlowSensorNotifier:
    def __init__(self, sensor, broker, port):
        self.sensor = sensor
        self.client = mqtt.Client(client_id=f"WaterFlowSensor-{self.sensor.get_sensor_id()}.notifier")
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

    def notify_flow_rate(self, room_number, flow_rate):
        payload = {"room_id": room_number, "type": "water", "flow_rate": flow_rate}
        self.client.publish(f"hotel/rooms/{room_number}/consumption", json.dumps(payload))
        logger.info(f"Flow rate notification sent for room {room_number} with flow rate {flow_rate}")
