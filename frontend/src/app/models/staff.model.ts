import { Task } from "./task.model";

export enum StaffRole {
    Cleaning = "cleaning",
    Security = "security",
    Maintenance = "maintenance",
}

export interface Staff {
    id: number;
    name: string;
    role: StaffRole;
    working: boolean;
    salary: number;
    phoneNumber: string;
    email: string;
    tasks: Task[];
}