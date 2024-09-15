from app.SmartClient.SmartClientNotifier import SmartClientNotifier
from app.SmartClient.SmartClientSubscriber import SmartClientSubscriber

import os
from dotenv import load_dotenv
load_dotenv()

class SmartClient():
    def __init__(self, client_id, first_name, last_name ,email):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.rfid_code = None
        self.room_number = None
        
        self.current_sum = 0
        self.flow_rate_sum = 0

        self.notifier = SmartClientNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = SmartClientSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def getClientId(self):
        return self.client_id

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name

    def getRfidCode(self):
        return self.rfid_code

    def getRoom(self):
        return self.room_number
    
    def getCurrentSum(self):
        return self.current_sum
    
    def getFlowRateSum(self):
        return self.flow_rate_sum

    def setRfidCode(self, rfid_code):
        if self.rfid_code:
            print(f"Client {self.client_id} changed RFID code from {self.rfid_code} to {rfid_code}")
        self.rfid_code = rfid_code

    def setFirstName(self, first_name):
        self.first_name = first_name

    def setLastName(self, last_name):
        self.last_name = last_name
    
    def addCurrent(self, current):
        self.current_sum += current
    
    def addFlowRate(self, flow_rate):
        self.flow_rate_sum += flow_rate
    
    def setRoom(self, room_number):
        if self.room_number:
            print(f"Client {self.client_id} changed room from {self.room_number} to {room_number}")
            self.notifier.notify_checkout(self.client_id, self.room_number)
            self.subscriber.unsubscribe(f"hotel/rooms/{self.room_number}/#")
        
        self.room_number = room_number
        self.notifier.notify_checkin(self.client_id, self.rfid_code, self.room_number)
        self.subscriber.subscribe(f"hotel/rooms/{self.room_number}/#")

    def checkin(self, rfid_code, room):
        if self.room_number:
            raise Exception(f"Client {self.client_id} is already checked in to room {self.room_number}")
        self.setRfidCode(rfid_code)
        self.setRoom(room)

    def checkout(self):
        self.notifier.notify_checkout(self.client_id, self.room_number)
        self.rfid_code = None
        self.room_number = None

    def adjust_environment(self,temperature, lighting_intensity):
        if not self.room_number:
            raise Exception(f"Client {self.client_id} is not checked in to any room")
        self.notifier.notify_adjust_environment(self.room_number, temperature, lighting_intensity)
        
    def requestRoomCleaning(self, room_id):
        if not self.room_number:
            raise Exception(f"Client {self.client_id} is not checked in to any room")
        self.notifier.notify_cleaning_request(self.room_number, room_id)

    def make_reservation(self, type, start_Date):
        self.notifier.notify_reservation(self.client_id, type, start_Date)
    
    def order_restaurant(self, order_details):
        self.notifier.notify_order(self.client_id, order_details)

    #TODO: Implementar estos mètodes ?
    def authenticate_rfid(self, rfid_code):
        if self.rfid_code == rfid_code:
            print(f"Client {self.client_id} authenticated with RFID code {rfid_code}")
            return True
        return False
    