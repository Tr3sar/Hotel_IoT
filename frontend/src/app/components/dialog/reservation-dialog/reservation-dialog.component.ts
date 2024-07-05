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
  datetime: any;

  constructor(
    private dialogRef: MatDialogRef<ReservationDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: number,
    private clientService: ClientService
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.clientService.makeReservation(this.data, this.reservation_type, this.datetime).subscribe(
      res => {
        this.dialogRef.close({res});
      }
    );
  }
}
