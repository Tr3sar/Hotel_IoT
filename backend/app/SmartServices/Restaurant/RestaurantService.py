from app.SmartServices.Restaurant.RestaurantServiceSubscriber import RestaurantServiceSubscriber

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class RestaurantService:
    def __init__(self):
        self.reservations = []
        self.subscriber = RestaurantServiceSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def make_reservation(self, client_id, time):
        exists, reservation_data = self.check_reservation_exists(client_id, time)

        if exists:
            self.reservations.append(reservation_data)
        else:
            url = os.getenv("API_URL") + f"/reservations"
            post_payload = {
                "client_id": client_id,
                "reservation_type": "restaurant",
                "start_date": time,
            }
            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
            }
            response = requests.post(url, headers=headers, json=post_payload)

            if response.status_code == 200:
                reservation = {"client_id": client_id, "time": time}
                self.reservations.append(reservation)

    def get_reservations(self):
        return self.reservations
    
    def check_reservation_exists(self, client_id, time):
        url = os.getenv("API_URL") + f"/reservations"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for reservation in data:
                if reservation['client_id'] == client_id and reservation['start_date'] == time and reservation['reservation_type'] == 'restaurant':
                    return True, reservation
        return False, None