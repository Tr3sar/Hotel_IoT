import paho.mqtt.client as mqtt
import json

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
        print(f"Sensor {self.sensor.get_sensor_id()}: Client connected to broker with result code {rc}")
    
    def on_disconnect(self, client, userdata, rc, properties=None):
        print(f"Sensor {self.sensor.get_sensor_id()}: Disconnected from broker with result code {rc}")
    
    def on_publish(self, client, userdata, mid, properties=None):
        print(f"Message published with ID: {mid}")

    def notify_flow_rate(self, sensor_id, flow_rate):
        payload = {"sensor_id": sensor_id, "flow_rate": flow_rate}
        self.client.publish(f"hotel/sensors/water/{sensor_id}/flow_rate", json.dumps(payload))
        print(f"Flow rate notification sent for sensor {sensor_id} with flow rate {flow_rate}")
