# app/Sensors/SmokeSensor/SmokeSensor.py

from app.Sensors.SmokeSensor.SmokeSensorNotifier import SmokeSensorNotifier
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

class SmokeSensor():
    def __init__(self, room_id):
        self.sensor_id = room_id
        self.smoke_level = 0
        self.smoke_detected = False
        self.notifier = SmokeSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.run()

    def get_sensor_id(self):
        return self.sensor_id

    def read_smoke_level(self):
        if self.smoke_detected:
            # Generar un valor alto para simular la detección de humo
            self.smoke_level = random.uniform(51, 100)
        else:
            # Generar valores por debajo del umbral
            self.smoke_level = random.uniform(0, 49)
        return self.smoke_level

    def check_for_smoke(self):
        # Definimos un umbral para la detección de humo
        THRESHOLD = 50.0
        if self.smoke_level > THRESHOLD:
            self.notifier.notify_smoke_detected(self.sensor_id, self.smoke_level)
            time.sleep(5)
            self.reset_smoke_detection()

    def trigger_smoke_detection(self):
        self.smoke_detected = True
    
    def reset_smoke_detection(self):
        self.smoke_detected = False

    def run(self):
        while True:
            self.read_smoke_level()
            self.check_for_smoke()
            time.sleep(5)