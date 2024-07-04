import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-order-restaurant-dialog',
  templateUrl: './order-restaurant-dialog.component.html',
  styleUrl: './order-restaurant-dialog.component.scss'
})
export class OrderRestaurantDialogComponent {
  order_details: string = '';

  constructor(
    private dialogRef: MatDialogRef<OrderRestaurantDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: number
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.dialogRef.close({
      order_details: this.order_details
    });
  }
}
