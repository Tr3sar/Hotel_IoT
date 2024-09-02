import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RoomAssignment } from '../models/room_assignment.model';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RoomAssignmentService {

  private apiUrl = 'http://localhost:8000/room_assignments';

  constructor(private http: HttpClient) { }

  getRoomAssignments() : Observable<RoomAssignment[]>{
    return this.http.get<RoomAssignment[]>(this.apiUrl)
  }
}
