import time
from app.SmartRoom.SmartRoom import SmartRoom

if __name__ == '__main__':
    room = SmartRoom(3)

    while True:
        time.sleep(1)

def start_room(number):
    room = SmartRoom(number)
    return room