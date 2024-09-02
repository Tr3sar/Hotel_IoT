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
import { switchMap } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  rooms: Room[] = [];
  clients: Client[] = [];
  roomAssignments: RoomAssignment[] = [];

  viewRooms: boolean = true;

  constructor(
    private clientService: ClientService,
    private roomService: RoomService,
    private roomAssignmentService: RoomAssignmentService,
    private dialog: MatDialog
  ) { }

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
      this.roomAssignments = roomAssignments.filter((roomAssignment: RoomAssignment) => roomAssignment.check_out_date == null);
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

  simulateFire(roomId: number): void {
    this.roomService.simulateFire(roomId).subscribe(
      
    );
  }

  checkout(client_id: number): void {
    let room_id = this.roomAssignments.find((roomAssignment: RoomAssignment) => roomAssignment.client_id === client_id)!.room_id;
    let room_number = this.rooms.find((room: Room) => room.id === room_id)!.number;
    let rfid_code = this.roomAssignments.find((roomAssignment: RoomAssignment) => roomAssignment.client_id === client_id)!.rfid_code;

    this.roomAssignments = this.roomAssignments.filter((roomAssignment: RoomAssignment) => roomAssignment.client_id !== client_id);
    this.clientService.checkoutClient(client_id, room_number, rfid_code).subscribe();
  }

  requestCleaning(): void {
    console.warn('TODO: Implement requestCleaning() method');
  }

  openDialog(type: string, data: any): void {
    let dialogRef;

    switch (type) {
      case 'checkin':
        dialogRef = this.dialog.open(CheckinDialogComponent, {
          data: data
        });

        dialogRef.afterClosed().subscribe(result => {
          if (result === undefined) return;
          console.table(result);
          let roomId = this.rooms.find((room: Room) => room.number == result.room_number)!.id;
          let lastAssignment = this.roomAssignments[this.roomAssignments.length - 1];
          let lastAssignmentId = lastAssignment ? lastAssignment.id : 0;
          const now = new Date();
    
          const year = now.getFullYear();
          const month = String(now.getMonth() + 1).padStart(2, '0');
          const day = String(now.getDate()).padStart(2, '0');

          const hours = String(now.getHours()).padStart(2, '0');
          const minutes = String(now.getMinutes()).padStart(2, '0');
          const seconds = String(now.getSeconds()).padStart(2, '0');

          const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
          let roomAssignment = {'client_id': result.client_id, 'room_id': roomId, 'rfid_code': result.rfid_code, 'expense': 0, 'check_in_date': formattedDateTime, 'check_out_date': null, id: lastAssignmentId + 1 || 1}
          this.roomAssignments.push(roomAssignment);
        });
        break;

      case 'reservation':
        dialogRef = this.dialog.open(ReservationDialogComponent, {
          data: data
        });

        dialogRef.afterClosed().subscribe(result => {
          console.table(result);
        });
        break;
      case 'order_restaurant':
        dialogRef = this.dialog.open(OrderRestaurantDialogComponent, {
          data: data
        });

        dialogRef.afterClosed().subscribe(result => {
          console.table(result);
        });
        break;
      case 'adjust_environment':
        dialogRef = this.dialog.open(AdjustEnvironmentDialogComponent, {
          data: data
        });

        dialogRef.afterClosed().subscribe(result => {
          console.table(result);
        });
        break;
      default:
        console.error('Invalid dialog type');
        return;
    }
  }
}
