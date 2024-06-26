from app.Sensors.SmokeSensor.SmokeSensorNotifier import SmokeSensorNotifier
import random
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

class SmokeSensor():
    def __init__(self, room_number):
        self.sensor_id = room_number
        self.smoke_level = 0
        self.smoke_detected = False
        self.notifier = SmokeSensorNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def get_sensor_id(self):
        return self.sensor_id

    def read_smoke_level(self):
        if self.smoke_detected:
            self.smoke_level = random.uniform(51, 100)
        else:
            self.smoke_level = random.uniform(0, 49)
        return self.smoke_level

    def check_for_smoke(self):
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