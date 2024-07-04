import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

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
    @Inject(MAT_DIALOG_DATA) public data: number
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.dialogRef.close({
      temperature: this.temperature,
      lighting_intensity: this.lighting_intensity
    });
  }
}
