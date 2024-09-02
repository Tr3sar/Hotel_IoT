import { Component } from '@angular/core';
import { Router } from '@angular/router';;
import { Task, TaskStatus } from '../../models/task.model';
import { Staff } from '../../models/staff.model';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.scss'
})
export class TasksComponent {
  tasks: Task[] = [];
  staff_member!: Staff;

  constructor(private router: Router, private taskService: TaskService) {
    const navigation = this.router.getCurrentNavigation();

    this.staff_member = navigation?.extras.state?.['staff_member'] as Staff;
    this.tasks = this.staff_member.tasks.filter(t => t.task_status !== TaskStatus.Completed);
  }

  get tasksNotCompleted() {
    return this.tasks.filter(t => t.task_status !== TaskStatus.Completed);
  }

  completeTask(task: Task): void {
    const now = new Date();
    
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    
    task.completedAt = formattedDateTime;
    task.task_status = TaskStatus.Completed

    this.taskService.updateTask(task).subscribe(() => {
      this.tasks = this.tasksNotCompleted;
    });
  }

  startTask(task: Task): void {
    task.task_status = TaskStatus.InProgress;

    this.taskService.updateTask(task).subscribe(() => {
      this.tasks = this.tasksNotCompleted;
    });
  }

}
