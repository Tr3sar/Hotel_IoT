from app.SmartRoom.SmartRoomSubscriber import SmartRoomSubscriber

from app.SmartRoom.RoomStatus import RoomStatus

from app.Devices.AC.AC import AC
from app.Devices.Bulb.Bulb import Bulb
from app.Sensors.ElectricityConsumptionSensor.ElectricityConsumptionSensor import ElectricityConsumptionSensor
from app.Sensors.WaterFlowSensor.WaterFlowSensor import WaterFlowSensor
from app.Sensors.SmokeSensor.SmokeSensor import SmokeSensor

import requests
import os
from dotenv import load_dotenv
load_dotenv()

class SmartRoom():
    def __init__(self, id, number):
        self.id = id
        self.number = number
        self.occupied_by = None
        self.assignment_id = None
        self.status = RoomStatus.CLEAN.value

        self.ac = AC(self.number)
        self.bulb = Bulb(self.number)

        #self.electricity_consumption_sensor = ElectricityConsumptionSensor(self.number)
        #self.water_flow_sensor = WaterFlowSensor(self.number)
        self.smoke_sensor = SmokeSensor(self.number)

        self.subscriber = SmartRoomSubscriber(self, os.getenv("BROKER_URL"), int(os.getenv("BROKER_PORT")))
    
    def get_number(self):
        return self.number
    
    def get_occupied_by(self):
        return self.occupied_by

    def adjust_environment(self, temperature, lightning_intensity):
        self.ac.set_temperature(temperature)
        self.bulb.set_intensity(lightning_intensity)

        url = os.getenv("API_URL") + f"/rooms/{self.id}/devices"
        put_payload = f'{{"temperature":"{temperature}", "lighting_intensity":"{lightning_intensity}"}}'
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "es",
        }
        response = requests.put(url, headers=headers, data=put_payload)

    def occupy(self, client_id, rfid_code):
        url = os.getenv("API_URL") + f"/room_assignment"
        put_payload = f'{{"client_id":"{client_id}", "room_number":"{self.number}", rfid_code":"{rfid_code}"}}'
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "es",
        }
        response = requests.put(url, headers=headers, data=put_payload)

        self.assignment_id = response.json()["id"]
        self.occupied_by = client_id
        #self.electricity_consumption_sensor.set_tracking_consumption(True)
        #self.water_flow_sensor.set_tracking_consumption(True)

    def vacate(self, client_id, rfid_code):
        if self.occupied_by == client_id and self.assignment_id is not None:
            url = os.getenv("API_URL") + f"/room_assignment/{self.assignment_id}"

            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
            }
            response = requests.delete(url, headers=headers)

            self.occupied_by = None
            self.assignment_id = None
            #self.electricity_consumption_sensor.set_tracking_consumption(False)
            #self.water_flow_sensor.set_tracking_consumption(False)
    
    def setRoomStatus(self, status):
        if status in [status.value for status in RoomStatus]:
            self.status = status
            
            url = os.getenv("API_URL") + f"/rooms/{self.number}/status"
            put_payload = f'{{"status":"{status}"}}'
            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "es",
            }
            response = requests.put(url, headers=headers, data=put_payload)
        else:
            print("Invalid room status")