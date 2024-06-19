from app.Sensors.ElectricityConsumptionSensor.ElectricityConsumptionSensorNotifier import ElectricityConsumptionSensorNotifier
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

class ElectricityConsumptionSensor():
    def __init__(self, room_id):
        self.sensor_id = room_id
        self.voltage = 0  # Señal analógica simulada
        self.current = 0  # Corriente calculada después de ADC (Analog to Digital Conversion)
        self.consumption_data = 0
        self.notifier = ElectricityConsumptionSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.run_mock_data()

    def get_sensor_id(self):
        return self.sensor_id

    def read_voltage(self):
        # Simular la lectura de la tensión generando valores aleatorios
        # El sensor SCT013 produce una señal de salida proporcional a la corriente medida
        self.voltage = random.uniform(0.0, 1.0)  # Simulación de señal analógica en voltios (0-1V)
        return self.voltage

    def convert_to_current(self):
        # Convertir la señal analógica a corriente
        # Suponemos un factor de conversión de 100A por 1V de salida
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
            self.read_voltage()
            self.convert_to_current()
            self.notify_current()
            time.sleep(10)