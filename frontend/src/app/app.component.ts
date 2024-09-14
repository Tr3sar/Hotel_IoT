import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NotifyDialogComponent } from './components/dialog/notify-dialog/notify-dialog.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {

  constructor(private dialog: MatDialog) {}

  notifyEvent() {
    let dialogRef = this.dialog.open(NotifyDialogComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
