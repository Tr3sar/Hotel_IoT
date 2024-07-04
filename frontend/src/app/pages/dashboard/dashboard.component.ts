import { Component, OnInit } from '@angular/core';
import { Room } from '../../models/room.model';
import { Client } from '../../models/client.model';
import { ClientService } from '../../services/client.service';
import { RoomService } from '../../services/room.service';
import { RoomAssignment } from '../../models/room_assignment.model';
import { RoomAssignmentService } from '../../services/room-assignment.service';
import { MatDialog } from '@angular/material/dialog';
import { CheckinDialogComponent } from '../../components/dialog/checkin-dialog/checkin-dialog.component';
import { ReservationDialogComponent } from '../../components/dialog/reservation-dialog/reservation-dialog.component';
import { OrderRestaurantDialogComponent } from '../../components/dialog/order-restaurant/order-restaurant-dialog.component';
import { AdjustEnvironmentDialogComponent } from '../../components/dialog/adjust-environment/adjust-environment-dialog.component';

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

  constructor(
    private clientService: ClientService,
    private roomService: RoomService,
    private roomAssignmentService: RoomAssignmentService,
    private dialog: MatDialog  
  ) {}

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

  simulateFire(): void {
    console.warn('TODO: Implement simulateFire() method');
  }

  checkout(): void {
    console.warn('TODO: Implement checkout() method');
  }

  requestCleaning(): void {
    console.warn('TODO: Implement requestCleaning() method');
  }

  openDialog(type: string, id: number): void{
    let dialogRef;

    switch(type) {
      case 'checkin':
        dialogRef = this.dialog.open(CheckinDialogComponent, {
          data: id
        });
        break;
      
      case 'reservation':
        dialogRef = this.dialog.open(ReservationDialogComponent, {
          data: id
        });
        break;
      case 'order_restaurant':
        dialogRef = this.dialog.open(OrderRestaurantDialogComponent, {
          data: id
        });
        break;
      case 'adjust_environment':
        dialogRef = this.dialog.open(AdjustEnvironmentDialogComponent, {
          data: id
        });
        break;
      default:
        console.error('Invalid dialog type');
        return;
    }

    dialogRef.afterClosed().subscribe(result => {
      console.table(result);
    });
  }
}
