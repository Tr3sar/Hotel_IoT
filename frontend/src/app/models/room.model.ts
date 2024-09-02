export enum RoomType {
  Single = "single",
  Double = "double",
  Suite = "suite",
}

export enum RoomStatus {
  Available = "available",
  Occupied = "occupied",
  Maintenance = "maintenance",
}

export interface Room {
  id: number;
  number: number;
  type: RoomType;
  status: RoomStatus;
  price: number;
  floor: number;
  description?: string;
  maxOccupancy: number;
  lastMaintenance?: string;
}
