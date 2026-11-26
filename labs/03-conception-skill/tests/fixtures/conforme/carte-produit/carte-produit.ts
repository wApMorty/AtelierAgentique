import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

@Component({
  selector: 'app-carte-produit',
  templateUrl: './carte-produit.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CarteProduit {
  readonly nom = input.required<string>();
  readonly prix = input.required<number>();
  readonly ajoute = output<void>();
}
