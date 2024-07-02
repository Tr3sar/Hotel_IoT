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

  constructor(private clientService: ClientService, private roomService: RoomService) {}

  ngOnInit() {
    
  }
}
