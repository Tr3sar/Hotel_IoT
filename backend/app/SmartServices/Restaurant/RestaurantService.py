from app.SmartServices.Restaurant.RestaurantServiceSubscriber import RestaurantServiceSubscriber

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class RestaurantService:
    def __init__(self):
        self.reservations = []
        self.subscriber = RestaurantServiceSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def make_reservation(self, client_id, time, special_request):
        exists, reservation_data = self.check_reservation_exists(client_id, time)

        if exists:
            self.reservations.append(reservation_data)
        else:
            url = os.getenv("API_URL") + f"/reservations"
            start_date = datetime.fromisoformat(time)
            end_date = start_date + timedelta(hours=2)
            
            post_payload = {
                "client_id": client_id,
                "type": "restaurant",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "status": "confirmed",
                "payment_status": "pending",
                "total_cost": 0,
                "special_request": special_request
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
                if reservation['client_id'] == client_id and reservation['start_date'] == time and reservation['type'] == 'restaurant':
                    return True, reservation
        return False, None