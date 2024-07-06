from app.Sensors.WaterFlowSensor.WaterFlowSensorNotifier import WaterFlowSensorNotifier
import random
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

class WaterFlowSensor():
    #Sensor YF-S201
    def __init__(self, room_id):
        self.sensor_id = room_id
        self.flow_rate = 0
        self.flow_rate_sum = 0

        self.tracking_consumption = False

        self.notifier = WaterFlowSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.thread = threading.Thread(target=self.run_mock_data)
        self.thread.start()

    def get_sensor_id(self):
        return self.sensor_id
    
    def set_tracking_consumption(self, tracking):
        self.tracking_consumption = tracking

    def read_flow_rate(self):
        # Simular la lectura del caudal d'aigua generant pols aleatoris
        pulses = random.randint(10, 450)
        # Convertir els pols a litres per minut (1 pols = 1/450 litre)
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
            if self.tracking_consumption:
                self.read_flow_rate()
                self.notify_flow_rate()
            time.sleep(10)
