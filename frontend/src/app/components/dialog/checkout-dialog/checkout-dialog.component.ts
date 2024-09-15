import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ClientService } from '../../../services/client.service';
import { RoomAssignmentService } from '../../../services/room-assignment.service';

@Component({
  selector: 'app-checkout-dialog',
  templateUrl: './checkout-dialog.component.html',
  styleUrl: './checkout-dialog.component.scss'
})
export class CheckoutDialogComponent {

  client_current_average: number = 0;
  client_flow_rate_average: number = 0;
  total_current_average: number = 0;
  total_flow_rate_average: number = 0;

  message: string = '';



  constructor(
    private dialogRef: MatDialogRef<CheckoutDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private clientService: ClientService,
    private roomAssignmentService: RoomAssignmentService
  ) {
    this.roomAssignmentService.getConsumption(this.data.roomAssignmentId).subscribe(
      res => {
        console.table(res)
        this.client_current_average = res.client_current_average;
        this.client_flow_rate_average = res.client_flow_rate_average;
        this.total_current_average = res.total_current_average;
        this.total_flow_rate_average = res.total_flow_rate_average;

        let clientTotalConsumption = this.client_current_average + this.client_flow_rate_average;
        let totalAverageConsumption = this.total_current_average + this.total_flow_rate_average;

        let isEligibleForOffer = clientTotalConsumption < totalAverageConsumption;

        if (isEligibleForOffer) {
          this.message = `Your total consumption (${clientTotalConsumption} units) is lower than the average (${totalAverageConsumption} units). You are eligible for a discount!`;
        } else {
          this.message = `Your total consumption (${clientTotalConsumption} units) exceeds the average (${totalAverageConsumption} units). Thank you for your stay!`;
        }
      });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    this.clientService.checkoutClient(this.data.client_id, this.data.room_number, this.data.rfid_code).subscribe(
      res => {
        this.dialogRef.close({client_id: this.data.client_id, room_number: this.data.room_number, rfid_code: this.data.rfid_code});
      }
    );
  }
}
