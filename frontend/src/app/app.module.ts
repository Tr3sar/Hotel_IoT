import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConsumptionComponent } from './pages/consumption/consumption.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';

import { AdjustEnvironmentDialogComponent } from './components/dialog/adjust-environment/adjust-environment-dialog.component';
import { CheckinDialogComponent } from './components/dialog/checkin-dialog/checkin-dialog.component';
import { ReservationDialogComponent } from './components/dialog/reservation-dialog/reservation-dialog.component';
import { OrderRestaurantDialogComponent } from './components/dialog/order-restaurant/order-restaurant-dialog.component';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import {MatSidenavModule} from '@angular/material/sidenav';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatIconModule} from '@angular/material/icon';
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import {MatDialogModule} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { StaffComponent } from './pages/staff/staff.component';
import { TasksComponent } from './pages/tasks/tasks.component';
import { NotifyDialogComponent } from './components/dialog/notify-dialog/notify-dialog.component';
import { CheckoutDialogComponent } from './components/dialog/checkout-dialog/checkout-dialog.component';



@NgModule({
  declarations: [
    AppComponent,
    ConsumptionComponent,
    DashboardComponent,
    AdjustEnvironmentDialogComponent,
    CheckinDialogComponent,
    ReservationDialogComponent,
    OrderRestaurantDialogComponent,
    StaffComponent,
    TasksComponent,
    NotifyDialogComponent,
    CheckoutDialogComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,

    MatSidenavModule,
    MatTooltipModule,
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatOptionModule,
    MatSelectModule
  ],
  providers: [
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
