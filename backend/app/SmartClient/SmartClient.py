from app.SmartClient.SmartClientNotifier import SmartClientNotifier
from app.SmartClient.SmartClientSubscriber import SmartClientSubscriber

import os
from dotenv import load_dotenv
load_dotenv()

class SmartClient():
    def __init__(self, client_id, name, email):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.rfid_code = None
        self.room_number = None

        self.notifier = SmartClientNotifier(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
        self.subscriber = SmartClientSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))

    def getClientId(self):
        return self.client_id

    def getName(self):
        return self.name

    def getRfidCode(self):
        return self.rfid_code

    def getRoom(self):
        return self.room_number

    def setRfidCode(self, rfid_code):
        if self.rfid_code:
            print(f"Client {self.client_id} changed RFID code from {self.rfid_code} to {rfid_code}")
        self.rfid_code = rfid_code

    def setName(self, name):
        print(f"Client {self.client_id} changed name from {self.name} to {name}")
        self.name = name
    
    def setRoom(self, room_number):
        if self.room_number:
            print(f"Client {self.client_id} changed room from {self.room_number} to {room_number}")
            self.notifier.notify_checkout(self.client_id, self.room_number)
            self.subscriber.unsubscribe(f"hotel/rooms/{self.room_number}/status")
        
        self.room_number = room_number
        self.notifier.notify_checkin(self.client_id, self.rfid_code, self.room_number)
        self.subscriber.subscribe(f"hotel/rooms/{self.room_number}/status")

    def checkin(self, rfid_code, room):
        if self.room_number:
            raise Exception(f"Client {self.client_id} is already checked in to room {self.room_number}")
        self.setRfidCode(rfid_code)
        self.setRoom(room)
        print(f"Client {self.name} checked in with RFID {rfid_code} in room {self.room_number}")

    def checkout(self):
        print(f"Client {self.name} checked out from room {self.room_number}")
        self.rfid_code = None
        self.room_number = None
        self.notifier.notify_checkout(self.client_id, self.room_number)

    def adjust_environment(self,temperature, lighting_intensity):
        if not self.room_number:
            raise Exception(f"Client {self.client_id} is not checked in to any room")
        self.notifier.notify_adjust_environment(self.room_number, temperature, lighting_intensity)
        print(f"Client {self.name} adjusted environment in room {self.room_number} to temperature {temperature} and lighting intensity {lighting_intensity}")

    def requestRoomCleaning(self):
        if not self.room_number:
            raise Exception(f"Client {self.client_id} is not checked in to any room")
        self.notifier.notify_cleaning_request(self.room_number)
        print(f"Client {self.name} requested cleaning for room {self.room_number}")

    #TODO: Implementar estos mètodes
    def make_reservation(self, reservation_id, reservation_type, start_Date):
        #Falta notificar, bbdd ja està fet en storage
        print(f"Client {self.name} made a reservation with id {reservation_id} of type {reservation_type} starting on {start_Date}")

    def authenticate_rfid(self, rfid_code):
        if self.rfid_code == rfid_code:
            print(f"Client {self.client_id} authenticated with RFID code {rfid_code}")
            return True
        return False
    