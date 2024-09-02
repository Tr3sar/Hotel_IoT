export interface RoomAssignment {
    id: number;
    client_id: number;
    room_id: number;
    rfid_code: number;
    expense: number;
    check_in_date: string;
    check_out_date: string | null;
}