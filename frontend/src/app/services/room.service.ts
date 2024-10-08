import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Room } from '../models/room.model';

@Injectable({
  providedIn: 'root'
})
export class RoomService {
  private apiUrl = 'http://localhost:8000/rooms';
  private simulationApiUrl = 'http://localhost:8000/simulation/rooms';

  constructor(private http: HttpClient) { }

  getRooms(): Observable<Room[]> {
    return this.http.get<Room[]>(this.apiUrl)
  }

  createRoom(room: Room): Observable<Room> {
    return this.http.post<Room>(this.apiUrl, room)
  }

  setRoomStatus(roomNumber: number, status: string): Observable<Room> {
    return this.http.put<Room>(`${this.apiUrl}/${roomNumber}/status`, { status })
  }

  adjustEnvironment(roomNumber: number, temperature: number, lightingIntensity: number): Observable<{temperature: number, lighting_intensity: number}> {
    return this.http.put<{temperature: number, lighting_intensity: number}>(`${this.simulationApiUrl}/${roomNumber}/environment`, { temperature, lighting_intensity: lightingIntensity })
  }

  simulateFire(roomId: number): Observable<{message: string}> {
    return this.http.put<{message: string}>(`${this.simulationApiUrl}/${roomId}/simulate-fire`, {})
  }
}
