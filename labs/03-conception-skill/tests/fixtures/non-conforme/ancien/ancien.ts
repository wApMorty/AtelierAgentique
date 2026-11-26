import { Component, Input, NgModule } from '@angular/core';

@Component({
  selector: 'ancien-widget',
  template: '<p>{{ titre }}</p>',
  standalone: false,
})
export class Ancien {
  @Input() titre = '';
}

@NgModule({ declarations: [Ancien] })
export class AncienModule {}
