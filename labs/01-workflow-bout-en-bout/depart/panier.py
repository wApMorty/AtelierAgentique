"""Panier d'achat minimal. Les montants sont en centimes pour éviter les erreurs d'arrondi."""


class Panier:
    def __init__(self) -> None:
        self._lignes: dict[str, tuple[int, int]] = {}

    def ajouter(self, article: str, prix_unitaire: int, quantite: int = 1) -> None:
        if prix_unitaire < 0 or quantite <= 0:
            raise ValueError("prix négatif ou quantité nulle")
        _, deja = self._lignes.get(article, (prix_unitaire, 0))
        self._lignes[article] = (prix_unitaire, deja + quantite)

    def total(self) -> int:
        return sum(prix * quantite for prix, quantite in self._lignes.values())
