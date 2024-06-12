from app.SmartServices.Restaurant.RestaurantServiceSubscriber import RestaurantServiceSubscriber
import os
from dotenv import load_dotenv

load_dotenv()

class RestaurantService:
    def __init__(self):
        self.reservations = []
        self.subscriber = RestaurantServiceSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def make_reservation(self, client_id, time):
        reservation = {"client_id": client_id, "time": time}
        self.reservations.append(reservation)

    def get_reservations(self):
        return self.reservations