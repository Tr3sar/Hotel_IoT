import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Staff } from '../models/staff.model';

@Injectable({
  providedIn: 'root'
})
export class StaffService {
  private apiUrl = 'http://localhost:8000/staff';
  private simulateApiUrl = 'http://localhost:8000/simulation/staff';

  constructor(private http: HttpClient) { }

  getStaff(): Observable<Staff[]> {
    return this.http.get<any>(this.apiUrl);
  }

  createStaff(staff: Staff): Observable<any> {
    return this.http.post<any>(this.apiUrl, staff);
  }

  startShift(staffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${staffId}/start-shift`, {});
  }

  endShift(staffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${staffId}/end-shift`, {});
  }

  completeTask(staffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${staffId}/complete-task`, {});
  }
}
