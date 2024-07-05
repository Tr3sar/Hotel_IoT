import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { RoomService } from '../../../services/room.service';

@Component({
  selector: 'app-adjust-environment-dialog',
  templateUrl: './adjust-environment-dialog.component.html',
  styleUrl: './adjust-environment-dialog.component.scss'
})
export class AdjustEnvironmentDialogComponent {
  temperature: number = 20;
  lighting_intensity: number = 100;

  constructor(
    private dialogRef: MatDialogRef<AdjustEnvironmentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private roomService: RoomService
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {;
    this.roomService.adjustEnvironment(this.data.room_number, this.temperature, this.lighting_intensity).subscribe(
      res => {
        this.dialogRef.close({res});
      }
    );
  }
}
