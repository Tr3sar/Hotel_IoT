import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Client } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ClientService {
  private apiUrl = 'http://localhost:5000/clients';

  constructor(private http: HttpClient) { }

  getClients(): Observable<Client[]> {
    return this.http.get<Client[]>(this.apiUrl);
  }

  createClient(client: Client): Observable<Client> {
    return this.http.post<Client>(this.apiUrl, client);
  }
  
  checkinClient(clientId: number, roomNumber: number, rfidCode: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/check_in`, { number: roomNumber, rfid_code: rfidCode });
  }

  checkoutClient(clientId: number, roomNumber: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/check_out`, { number: roomNumber });
  }

  cleaningRequest(clientId: number, roomNumber: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/request_cleaning`, { number: roomNumber });
  }

  orderRestaurant(clientId: number, order_details: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/${clientId}/order_restaurant`, { order_details });
  }
}
