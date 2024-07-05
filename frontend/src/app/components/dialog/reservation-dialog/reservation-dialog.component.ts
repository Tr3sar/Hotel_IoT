import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ClientService } from '../../../services/client.service';

@Component({
  selector: 'app-reservation-dialog',
  templateUrl: './reservation-dialog.component.html',
  styleUrl: './reservation-dialog.component.scss'
})
export class ReservationDialogComponent {

  reservation_types: string[] = ['restaurant', 'spa'];
  reservation_type: string = 'restaurant';
  datetime: string;

  constructor(
    private dialogRef: MatDialogRef<ReservationDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private clientService: ClientService
  ) {
    const now = new Date();
    const options = {
      year: 'numeric' as const, 
      month: '2-digit' as const,
      day: '2-digit' as const,
      hour12: false,
      timeZone: 'Europe/Madrid'
    };
    const formattedDate = now.toLocaleDateString('en-GB', options).split('/').reverse().join('-');
    const formattedTime = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Europe/Madrid' });
    this.datetime = `${formattedDate}T${formattedTime}`;
    console.log(this.datetime);
  }

  onDateChange(event: any): void {
    const value = event.target.value;
    const year = parseInt(value.split('-')[0], 10);
    if (year > 9999) {
      this.datetime = value.slice(0, 4) + value.slice(5);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.clientService.makeReservation(this.data.client_id, this.reservation_type, this.datetime).subscribe(
      res => {
        this.dialogRef.close({ res });
      }
    );
    
  }
}
