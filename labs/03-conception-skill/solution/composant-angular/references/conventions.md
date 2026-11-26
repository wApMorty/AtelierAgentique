# Conventions de composant de l'équipe

Conventions fictives, propres à ce lab.

| Règle | Exemple |
|---|---|
| Fichiers `<nom>.ts`, `<nom>.html`, `<nom>.spec.ts` dans un dossier `<nom>/` | `carte-produit/carte-produit.ts` |
| Sélecteur préfixé `app-` et égal au nom | `selector: 'app-carte-produit'` |
| Composant autonome, jamais déclaré dans un `NgModule` | pas de `standalone: false` |
| Détection de changements `OnPush` | `changeDetection: ChangeDetectionStrategy.OnPush` |
| Entrées et sorties par fonctions | `prix = input.required<number>()`, `ajoute = output<void>()` |
| Aucun décorateur `@Input` ni `@Output` | — |

Exemple :

```ts
import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

@Component({
  selector: 'app-carte-produit',
  templateUrl: './carte-produit.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CarteProduit {
  readonly nom = input.required<string>();
  readonly ajoute = output<void>();
}
```
