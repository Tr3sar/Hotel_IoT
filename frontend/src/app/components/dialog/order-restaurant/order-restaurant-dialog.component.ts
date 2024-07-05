import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ClientService } from '../../../services/client.service';

@Component({
  selector: 'app-order-restaurant-dialog',
  templateUrl: './order-restaurant-dialog.component.html',
  styleUrl: './order-restaurant-dialog.component.scss'
})
export class OrderRestaurantDialogComponent {
  order_details: string = '';

  constructor(
    private dialogRef: MatDialogRef<OrderRestaurantDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private clientService: ClientService
  ) {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.clientService.orderRestaurant(this.data.client_id, this.order_details).subscribe(
      res => {
        this.dialogRef.close({res});
      }
    );
  }
}
