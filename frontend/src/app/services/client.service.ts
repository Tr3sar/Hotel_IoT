import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Client } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ClientService {
  private apiUrl = 'http://localhost:8000/clients';
  private simulateApiUrl = 'http://localhost:8000/simulation/clients';

  constructor(private http: HttpClient) { }

  getClients(): Observable<Client[]> {
    return this.http.get<Client[]>(this.apiUrl)
  }

  createClient(client: Client): Observable<Client> {
    return this.http.post<Client>(this.apiUrl, client)
  }
  
  checkinClient(clientId: number, roomNumber: number, rfidCode: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${clientId}/check_in`, { room_number: roomNumber, rfid_code: rfidCode })
  }

  checkoutClient(clientId: number, roomNumber: number, rfidCode: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${clientId}/check_out`, { room_number: roomNumber, rfid_code: rfidCode})
  }

  cleaningRequest(clientId: number, roomNumber: number): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${clientId}/request_cleaning`, { room_number: roomNumber })
  }

  orderRestaurant(clientId: number, order_details: string): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${clientId}/order_restaurant`, { order_details })
  }

  makeReservation(clientId: number, reservationType: string, datetime: any): Observable<any> {
    return this.http.put(`${this.simulateApiUrl}/${clientId}/reservation`, { client_id: clientId, reservation_type: reservationType, start_date: datetime })
  }
}
