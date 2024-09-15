import { Room } from "./room.model";

export enum TaskStatus {
    Pending = "pending",
    InProgress = "in_progress",
    Completed = "completed",
}

export interface Task {
    id: number;
    staff_id: number;
    room_id: number;
    task_status: TaskStatus;
    assigned_at: string;
    completed_at?: string;
    room: Room;
}
