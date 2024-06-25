from app.Sensors.ElectricityConsumptionSensor.ElectricityConsumptionSensorNotifier import ElectricityConsumptionSensorNotifier
import random
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

class ElectricityConsumptionSensor():
    def __init__(self, room_id):
        self.sensor_id = room_id
        self.voltage = 0  # Senyal analògica simulada en volts
        self.current = 0  # Corrent calculada després d'ADC (Analog to Digital Conversion)
        self.consumption_data = 0

        self.tracking_consumption = False

        self.notifier = ElectricityConsumptionSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.thread = threading.Thread(target=self.run_mock_data)
        self.thread.start()

    def get_sensor_id(self):
        return self.sensor_id

    def set_tracking_consumption(self, tracking):
        self.tracking_consumption = tracking
    
    def read_voltage(self):
        # Simular la lectura de la tensió generant valors al·leatoris
        # El sensor SCT013 produeix una senyal d'eixida proporcional a la corrent mesurada
        self.voltage = random.uniform(0.0, 1.0)  # Simulació de senyal analògica en volts (0-1V)
        return self.voltage

    def convert_to_current(self):
        # Convertir la senyal analògica a corrent
        # Suposem un factor de conversió de 100A per 1V d'eixida
        self.current = self.voltage * 100
        self.consumption_data += self.current
        return self.current
    
    def get_consumption_data(self):
        return self.consumption_data
    
    def clear_consumption_data(self):
        self.consumption_data = 0

    def notify_current(self):
        self.notifier.notify_current(self.sensor_id, self.current)

    def run_mock_data(self):
        while True:
            if self.tracking_consumption:
                self.read_voltage()
                self.convert_to_current()
                self.notify_current()
            time.sleep(10)