import time
from app.SmartClient.SmartClient import SmartClient

if __name__ == '__main__':
    client = SmartClient(3, "Josep Martín Torres")

    time.sleep(2)
    client.checkin("123456", 3)

    while True:
        time.sleep(1)

def start_client(client_id, name):
    client = SmartClient(client_id, name)
    return client