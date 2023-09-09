import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent {
  @Input() title: string = '';
  @Input() content: string = '';
  @Output() continue: EventEmitter<any> = new EventEmitter<any>();

  clickContinue() {
    this.continue.emit();
  }

}
