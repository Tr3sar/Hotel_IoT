import { Component, Input } from '@angular/core';
import { RoomService } from '../../services/room.service';
import { Room } from '../../models/room.model';

@Component({
  selector: 'app-room',
  templateUrl: './room.component.html',
  styleUrls: ['./room.component.scss']
})
export class RoomComponent {
  @Input() room!: Room;
  menuVisible = false;
  roomOptions = ['Set Status'];
  roomStatuses = ['clean', 'clean-required', 'cleaning'];
  selectedStatus: string = this.roomStatuses[0];

  constructor(private roomService: RoomService) {}

  toggleMenu() {
    this.menuVisible = !this.menuVisible;
  }

  handleOptionSelected(option: string) {
    if (option === 'Set Status') {
      this.setStatus(this.selectedStatus);
    }
    this.menuVisible = false;
  }

  setStatus(status: string) {
    this.roomService.setRoomStatus(this.room.number, status).subscribe(response => {
      console.log('Room status set:', response);
    });
  }
}
