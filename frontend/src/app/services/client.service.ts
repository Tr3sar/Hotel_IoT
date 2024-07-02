import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Client } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ClientService {
  private apiUrl = 'http://localhost:5000/api/clients';

  constructor(private http: HttpClient) { }

  createClient(client: Client): Observable<Client> {
    return this.http.post<Client>(this.apiUrl, client);
  }
  
  checkinClient(clientId: number, roomNumber: number, rfidCode: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/checkin`, { number: roomNumber, rfid_code: rfidCode });
  }

  checkoutClient(clientId: number, roomNumber: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/checkout`, { number: roomNumber });
  }

  adjustEnvironment(clientId: number, roomNumber: number, temperature: number, lightningIntensity: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/environment`, { number: roomNumber, temperature, lightning_intensity: lightningIntensity });
  }

  cleaningRequest(clientId: number, roomNumber: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/cleaning_request`, { number: roomNumber });
  }
}
