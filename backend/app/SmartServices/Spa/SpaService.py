from app.SmartServices.Spa.SpaServiceSubscriber import SpaServiceSubscriber

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SpaService:
    def __init__(self):
        self.appointments = []
        self.subscriber = SpaServiceSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def book_appointment(self, client_id, time):
        exists, appointment_data = self.check_appointment_exists(client_id, time)

        if exists:
            self.appointments.append(appointment_data)
        else:
            url = os.getenv("API_URL") + f"/reservations"
            post_payload = {
                "client_id": client_id,
                "type": "spa",
                "start_date": time,
            }
            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
            }
            response = requests.post(url, headers=headers, json=post_payload)

            if response.status_code == 200:
                appointment = {"client_id": client_id, "time": time}
                self.appointments.append(appointment)

    def get_appointments(self):
        return self.appointments
    
    def check_appointment_exists(self, client_id, time):
        url = os.getenv("API_URL") + f"/reservations"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for appointment in data:
                if appointment['client_id'] == client_id and appointment['start_date'] == time and appointment['type'] == 'spa':
                    return True, appointment
        return False, None