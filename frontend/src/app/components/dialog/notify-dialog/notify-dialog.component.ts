import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HotelService } from '../../../services/hotel.service';

@Component({
  selector: 'app-notify-dialog',
  templateUrl: './notify-dialog.component.html',
  styleUrl: './notify-dialog.component.scss'
})
export class NotifyDialogComponent {
  event_details: string = '';

  constructor(
    private dialogRef: MatDialogRef<NotifyDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private hotelService: HotelService
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.hotelService.notifyEvent(this.event_details).subscribe(
      res => {
        this.dialogRef.close({res});
      }
    );
  }
}
