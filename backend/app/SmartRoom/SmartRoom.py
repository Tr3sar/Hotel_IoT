from app.SmartRoom.SmartRoomSubscriber import SmartRoomSubscriber

from app.SmartRoom.RoomStatus import RoomStatus

from app.Devices.AC.AC import AC
from app.Devices.Bulb.Bulb import Bulb
from app.Sensors.ElectricityConsumptionSensor.ElectricityConsumptionSensor import ElectricityConsumptionSensor
from app.Sensors.WaterFlowSensor.WaterFlowSensor import WaterFlowSensor
from app.Sensors.SmokeSensor.SmokeSensor import SmokeSensor

import os
from dotenv import load_dotenv
load_dotenv()

class SmartRoom():
    def __init__(self, number):
        self.number = number
        self.occupied_by = None
        self.status = RoomStatus.CLEAN.value

        #TODO: Decidir si canviem les propietats d'AC i Bulb per MQTT o per self.ac.setTemperature(temperature)
        #self.temperature = 22
        #self.lightning_intensity = 100
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

    def occupy(self, client_id):
        self.occupied_by = client_id
        #self.electricity_consumption_sensor.set_tracking_consumption(True)
        #self.water_flow_sensor.set_tracking_consumption(True)
        print(f"Room {self.number} occupied by {self.occupied_by}")

    def vacate(self, client_id):
        if self.occupied_by == client_id:
            print(f"Room {self.number} vacated by {self.occupied_by}")
            self.occupied_by = None
            #self.electricity_consumption_sensor.set_tracking_consumption(False)
            #self.water_flow_sensor.set_tracking_consumption(False)
    
    def setRoomStatus(self, status):
        if status in [status.value for status in RoomStatus]:
            self.status = status
            print(f"Room {self.number} status set to {status}")
        else:
            print("Invalid room status")
            
    #borrar?
    def notifyRoomStatus(self, status):
        if status in [status.value for status in RoomStatus]:
            self.status = status
            self.notifier.notify_room_status(self.number, status)
            print(f"Room {self.number} status set to {status}")
        else:
            print("Invalid room status")