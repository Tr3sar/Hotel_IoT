import { Component } from '@angular/core';
import { ClientService } from './services/client.service';
import { RoomService } from './services/room.service';
import { Client } from './models/client.model';
import { Room } from './models/room.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  clients: Client[] = [];
  rooms: Room[] = [];

  clientsNames = ['John', 'Jane', 'Doe', 'Smith', 'Brown', 'Wilson', 'Johnson', 'Williams', 'Jones', 'Miller'];

  constructor(private clientService: ClientService, private roomService: RoomService) {}

  ngOnInit() {
    
  }

  addClient() {
    if (this.clients.length >= this.clientsNames.length - 1) return;
    const newClient = { id: this.clients.length + 1, name: this.clientsNames[this.clients.length + 1] };
    this.clientService.createClient(newClient).subscribe(response => {
      this.clients.push(response);
    });
  }

  addRoom() {
    const newRoom: Room = { number: this.rooms.length + 1};
    this.roomService.createRoom(newRoom).subscribe(response => {
      this.rooms.push(response);
    });
  }
}
