from app.Sensors.WaterFlowSensor.WaterFlowSensorNotifier import WaterFlowSensorNotifier
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

class WaterFlowSensor():
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.flow_rate = 0
        self.notifier = WaterFlowSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.run_mock_data()

    def get_sensor_id(self):
        return self.sensor_id

    def read_flow_rate(self):
        # Simular la lectura del caudal de agua generando pulsos aleatorios
        pulses = random.randint(10, 450)
        # Convertir los pulsos a litros por minuto (1 pulso = 1/450 litro)
        self.flow_rate = pulses / 450.0
        return self.flow_rate

    def notify_flow_rate(self):
        self.notifier.notify_flow_rate(self.sensor_id, self.flow_rate)
    
    def run_mock_data(self):
        while True:
            self.read_flow_rate()
            self.notify_flow_rate()
            time.sleep(10)
