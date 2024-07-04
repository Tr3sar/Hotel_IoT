import { Component, OnInit } from '@angular/core';
import { Room } from '../../models/room.model';
import { Client } from '../../models/client.model';
import { ClientService } from '../../services/client.service';
import { RoomService } from '../../services/room.service';
import { RoomAssignment } from '../../models/room_assignment.model';
import { RoomAssignmentService } from '../../services/room-assignment.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit{
  rooms: Room[] = [];
  clients: Client[] = [];
  roomAssignments: RoomAssignment[] = [];

  viewRooms: boolean = true;

  constructor(private clientService: ClientService, private roomService: RoomService, private roomAssignmentService: RoomAssignmentService) {}

  ngOnInit() {
    this.roomService.getRooms().subscribe((rooms: Room[]) => {
      this.rooms = rooms;
      console.table(this.rooms);
    });

    this.clientService.getClients().subscribe((clients: Client[]) => {
      this.clients = clients;
      console.table(this.clients);
    });

    this.roomAssignmentService.getRoomAssignments().subscribe((roomAssignments: RoomAssignment[]) => {
      this.roomAssignments = roomAssignments;
      console.table(this.roomAssignments);
    });
  }

  changeView(): void {
    this.viewRooms = !this.viewRooms;
  }

  isRoomOccupied(room_id: number): boolean {
    return this.roomAssignments.some((roomAssignment: RoomAssignment) => roomAssignment.room_id === room_id);
  }

  isClientInRoom(client_id: number): boolean {
    return this.roomAssignments.some((roomAssignment: RoomAssignment) => roomAssignment.client_id === client_id);
  }

  getClientByRoomId(room_id: number): Client | undefined {
    const roomAssignment = this.roomAssignments.find((roomAssignment: RoomAssignment) => roomAssignment.room_id === room_id);
    return this.clients.find((client: Client) => client.id === roomAssignment!.client_id);
  }

  getRoomByClientId(client_id: number): Room | undefined {
    const roomAssignment = this.roomAssignments.find((roomAssignment: RoomAssignment) => roomAssignment.client_id === client_id);
    return this.rooms.find((room: Room) => room.id === roomAssignment!.room_id);
  }
}
