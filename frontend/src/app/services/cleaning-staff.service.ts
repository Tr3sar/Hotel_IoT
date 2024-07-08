import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CleaningStaff } from '../models/cleaning_staff.model';

@Injectable({
  providedIn: 'root'
})
export class CleaningStaffService {
  private apiUrl = 'http://localhost:8000/cleaning_staff';
  private simulateApiUrl = 'http://localhost:8000/simulation/cleaning_staff';

  constructor(private http: HttpClient) { }

  getCleaningStaff(): Observable<CleaningStaff[]> {
    return this.http.get<any>(this.apiUrl);
  }

  createCleaningStaff(cleaningStaff: CleaningStaff): Observable<any> {
    return this.http.post<any>(this.apiUrl, cleaningStaff);
  }

  startShift(cleaningStaffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${cleaningStaffId}/start-shift`, {});
  }

  endShift(cleaningStaffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${cleaningStaffId}/end-shift`, {});
  }

  completeTask(cleaningStaffId: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${cleaningStaffId}/complete-task`, {});
  }
}
