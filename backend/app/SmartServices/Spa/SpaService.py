from app.SmartServices.Spa.SpaServiceSubscriber import SpaServiceSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class SpaService:
    def __init__(self):
        self.appointments = []
        self.subscriber = SpaServiceSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def book_appointment(self, client_id, time):
        appointment = {"client_id": client_id, "time": time}
        self.appointments.append(appointment)

    def get_appointments(self):
        return self.appointments