import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Task } from '../models/task.model';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private apiUrl = 'http://localhost:8000/tasks';

  constructor(private http: HttpClient) { }

  updateTask(task: Task): Observable<Task> {
    console.table(task);
    return this.http.put<Task>(`${this.apiUrl}/${task.id}`, task);
  }
}