import { Component, Input } from '@angular/core';
import { ClientService } from '../../services/client.service';
import { Client } from '../../models/client.model';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.scss']
})
export class ClientComponent {
  @Input() client!: Client;
  menuVisible = false;
  clientOptions = ['Check-in', 'Check-out', 'Adjust Environment', 'Cleaning Request'];
  selectedRoom: number | null = null;
  selectedRFID: number | null = null;
  temperature: number = 22;
  lightningIntensity: number = 75;

  constructor(private clientService: ClientService) {}

  toggleMenu() {
    this.menuVisible = !this.menuVisible;
  }

  handleOptionSelected(option: string) {
    if (option === 'Check-in') {
      this.checkin();
    } else if (option === 'Check-out') {
      this.checkout();
    } else if (option === 'Adjust Environment') {
      this.adjustEnvironment();
    } else if (option === 'Cleaning Request') {
      this.cleaningRequest();
    }
    this.menuVisible = false;
  }

  checkin() {
    if (this.selectedRoom !== null && this.selectedRFID !== null) {
      this.clientService.checkinClient(this.client.id, this.selectedRoom, this.selectedRFID).subscribe(response => {
        console.log('Check-in successful:', response);
      });
    } else {
      console.error('Room number is required for check-in.');
    }
  }

  checkout() {
    if (this.selectedRoom !== null) {
      this.clientService.checkoutClient(this.client.id, this.selectedRoom).subscribe(response => {
        console.log('Check-out successful:', response);
      });
    } else {
      console.error('Room number is required for check-out.');
    }
  }

  adjustEnvironment() {
    if (this.selectedRoom !== null) {
      this.clientService.adjustEnvironment(this.client.id, this.selectedRoom, this.temperature, this.lightningIntensity).subscribe(response => {
        console.log('Environment adjusted:', response);
      });
    } else {
      console.error('Room number is required for adjusting environment.');
    }
  }

  cleaningRequest() {
    if (this.selectedRoom !== null) {
      this.clientService.cleaningRequest(this.client.id, this.selectedRoom).subscribe(response => {
        console.log('Cleaning requested:', response);
      });
    } else {
      console.error('Room number is required for cleaning request.');
    }
  }
}
