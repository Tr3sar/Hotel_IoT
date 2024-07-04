import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Room } from '../models/room.model';

@Injectable({
  providedIn: 'root'
})
export class RoomService {
  private apiUrl = 'http://localhost:8000/rooms';

  constructor(private http: HttpClient) { }

  getRooms(): Observable<Room[]> {
    return this.http.get<Room[]>(this.apiUrl);
  }

  createRoom(room: Room): Observable<Room> {
    return this.http.post<Room>(this.apiUrl, room);
  }

  setRoomStatus(roomNumber: number, status: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/${roomNumber}/status`, { status });
  }

  adjustEnvironment(roomNumber: number, temperature: number, lightingIntensity: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${roomNumber}/environment`, { temperature, lighting_intensity: lightingIntensity });
  }

  simulateFire(roomId: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${roomId}/simulate_fire`, {});
  }
}
