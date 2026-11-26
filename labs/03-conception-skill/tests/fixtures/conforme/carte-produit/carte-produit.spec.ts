import { TestBed } from '@angular/core/testing';
import { CarteProduit } from './carte-produit';

describe('CarteProduit', () => {
  it('affiche le nom', () => {
    const fixture = TestBed.createComponent(CarteProduit);
    fixture.componentRef.setInput('nom', 'Livre');
    fixture.componentRef.setInput('prix', 1500);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Livre');
  });
});
