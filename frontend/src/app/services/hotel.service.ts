import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HotelService {

  private simulationApiUrl = 'http://localhost:8000/simulation/hotel';
  
  constructor(private http: HttpClient) { }

  notifyEvent(info: string): Observable<any> {
    return this.http.post(`${this.simulationApiUrl}/event`, { info });
  }
}
