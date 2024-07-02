import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HotelService {

  private apiUrl = 'http://localhost:5000/hotel';
  
  constructor(private http: HttpClient) { }

  notifyEvent(info: string): void {
    this.http.post(`${this.apiUrl}/event`, { info }).subscribe();
  }
}
