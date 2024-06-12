from flask import request, jsonify
from app import app
from app.SmartClient.SmartClientStarter import start_client
from app.SmartRoom.SmartRoomStarter import start_room
from app.SmartRoom.RoomStatus import RoomStatus
from app.storage import clients, rooms

@app.route('/api/clients', methods=['POST'])
def create_client():
    client = request.json
    client_id = client['id']
    client_name = client['name']

    client_instance = start_client(client_id, client_name)
    clients[client_id] = client_instance
    return jsonify({"id": client_id, "name": client_name}), 201

@app.route('/api/rooms', methods=['POST'])
def create_room():
    room = request.json
    room_number = room['number']

    room_instance = start_room(room_number)
    rooms[room_number] = room_instance
    return jsonify({"number": room_number}), 201

@app.route('/api/clients/<int:client_id>/checkin', methods=['PUT'])
def check_in(client_id):
    data = request.json
    room_number = data['number']
    rfid_code = data['rfid_code']
    if client_id in clients and room_number in rooms:
        clients[client_id].checkin(rfid_code, room_number)
        return jsonify({"message": "Check-in successful"}), 200
    return jsonify({"message": "Room or client not found"}), 404

@app.route('/api/clients/<int:client_id>/checkout', methods=['PUT'])
def check_out(client_id):
    data = request.json
    room_number = data['number']
    if client_id in clients and room_number in rooms:
        clients[client_id].checkout()
        return jsonify({"message": "Check-out successful"}), 200
    return jsonify({"message": "Room or client not found"}), 404

@app.route('/api/clients/<int:client_id>/environment', methods=['PUT'])
def adjust_environment(client_id):
    data = request.json
    temperature = data['temperature']
    lightning_intensity = data['lightning_intensity']
    if client_id in clients:
        clients[client_id].adjust_environment(temperature, lightning_intensity)
        return jsonify({"message": "Environment adjusted"}), 200
    return jsonify({"message": "Client not found"}), 404

@app.route('/api/clients/<int:client_id>/cleaning_request', methods=['PUT'])
def cleaning_request(client_id):
    data = request.json
    if client_id in clients:
        clients[client_id].requestRoomCleaning()
        return jsonify({"message": "Cleaning requested"}), 200
    return jsonify({"message": "Client not found"}), 404

@app.route('/api/rooms/<int:room_number>/status', methods=['PUT'])
def set_room_status(room_number):
    data = request.json
    status = data['status']
    if room_number in rooms:
        if status in RoomStatus:
            rooms[room_number].setRoomStatus(status)
            return jsonify({"message": "Room status set"}), 200
        return jsonify({"message": "Invalid status"}), 400
    return jsonify({"message": "Room not found"}), 404
