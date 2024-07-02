import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent {
  @Input() options: string[] = [];
  @Output() optionSelected = new EventEmitter<string>();

  selectOption(option: string) {
    this.optionSelected.emit(option);
  }
}
