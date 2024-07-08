import { Component } from '@angular/core';
import { CleaningStaffService } from '../../services/cleaning-staff.service';
import { CleaningStaff } from '../../models/cleaning_staff.model';

@Component({
  selector: 'app-staff',
  templateUrl: './staff.component.html',
  styleUrl: './staff.component.scss'
})
export class StaffComponent {
  cleaning_staff: CleaningStaff[] = [];

  constructor(private cleaningStaffService: CleaningStaffService) {
    this.cleaningStaffService.getCleaningStaff().subscribe((data: CleaningStaff[]) => {
      this.cleaning_staff = data;
    });
  }

  startShift(staff: CleaningStaff) {
    this.cleaningStaffService.startShift(staff.id).subscribe(() => {
      staff.working = true;
    });
  }

  endShift(staff: CleaningStaff) {
    this.cleaningStaffService.endShift(staff.id).subscribe(() => {
      staff.working = false;
    });
  }

  completeTask(staff: CleaningStaff) {
    this.cleaningStaffService.completeTask(staff.id).subscribe(() => {
    });
  }
}
