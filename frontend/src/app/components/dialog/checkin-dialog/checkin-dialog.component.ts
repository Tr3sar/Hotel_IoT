import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-checkin-dialog',
  templateUrl: './checkin-dialog.component.html',
  styleUrl: './checkin-dialog.component.scss'
})
export class CheckinDialogComponent {
  room_number: number = 0;
  rfid_code: number = 0;

  constructor(
    private dialogRef: MatDialogRef<CheckinDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: number
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.dialogRef.close({
      room_number: this.room_number,
      rfid_code: this.rfid_code
    });
  }
}
