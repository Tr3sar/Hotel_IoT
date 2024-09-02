import { Component } from '@angular/core';
import { StaffService } from '../../services/cleaning-staff.service';
import { Staff } from '../../models/staff.model';

@Component({
  selector: 'app-staff',
  templateUrl: './staff.component.html',
  styleUrl: './staff.component.scss'
})
export class StaffComponent {
  staff: Staff[] = [];

  constructor(private staffService: StaffService) {
    this.staffService.getStaff().subscribe((data: Staff[]) => {
      console.table(data);
      this.staff = data.sort((a, b) => {
        if (a.role === 'cleaning' && b.role !== 'cleaning') {
          return -1;
        } else if (a.role !== 'cleaning' && b.role === 'cleaning') {
          return 1;
        } else {
          return 0;
        }
      });
    });
  }

  get cleaning_staff() {
    return this.staff.filter(staff => staff.role === 'cleaning');
  }

  get security_staff() {
    return this.staff.filter(staff => staff.role === 'security');
  }

  startShift(staff: Staff) {
    this.staffService.startShift(staff.id).subscribe(() => {
      staff.working = true;
    });
  }

  endShift(staff: Staff) {
    this.staffService.endShift(staff.id).subscribe(() => {
      staff.working = false;
    });
  }

  completeTask(staff: Staff) {
    this.staffService.completeTask(staff.id).subscribe(() => {
    });
  }
}
