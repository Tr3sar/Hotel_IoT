import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ClientService } from '../../../services/client.service';

@Component({
  selector: 'app-checkin-dialog',
  templateUrl: './checkin-dialog.component.html',
  styleUrl: './checkin-dialog.component.scss'
})
export class CheckinDialogComponent {
  room_number: number = 100;
  rfid_code: number = 0;

  constructor(
    private dialogRef: MatDialogRef<CheckinDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private clientService: ClientService
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.clientService.checkinClient(this.data.client_id, this.room_number, this.rfid_code).subscribe(
      res => {
        this.dialogRef.close({client_id: this.data.client_id, room_number: this.room_number, rfid_code: this.rfid_code});
      }
    );
  }
}
