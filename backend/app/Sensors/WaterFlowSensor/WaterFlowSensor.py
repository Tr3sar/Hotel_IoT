from app.Sensors.WaterFlowSensor.WaterFlowSensorNotifier import WaterFlowSensorNotifier
import random
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

class WaterFlowSensor():
    def __init__(self, room_id):
        self.sensor_id = room_id
        self.flow_rate = 0
        self.flow_rate_sum = 0
        self.notifier = WaterFlowSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.thread = threading.Thread(target=self.run_mock_data)
        self.thread.start()

    def get_sensor_id(self):
        return self.sensor_id

    def read_flow_rate(self):
        # Simular la lectura del caudal de agua generando pulsos aleatorios
        pulses = random.randint(10, 450)
        # Convertir los pulsos a litros por minuto (1 pulso = 1/450 litro)
        self.flow_rate = pulses / 450.0
        self.flow_rate_sum += self.flow_rate
        return self.flow_rate
    
    def get_flow_rate_sum(self):
        return self.flow_rate_sum
    
    def clear_flow_rate_sum(self):
        self.flow_rate_sum = 0

    def notify_flow_rate(self):
        self.notifier.notify_flow_rate(self.sensor_id, self.flow_rate)
    
    def run_mock_data(self):
        while True:
            self.read_flow_rate()
            self.notify_flow_rate()
            time.sleep(10)
