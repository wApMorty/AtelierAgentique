"""Solution indicative du lab 01 : panier avec codes promo."""

CODES = {
    "POURCENT10": lambda total: total // 10,
    "MOINS5": lambda total: 500,
}
SEUIL_MOINS5 = 3000


class Panier:
    def __init__(self) -> None:
        self._lignes: dict[str, tuple[int, int]] = {}
        self._code: str | None = None

    def ajouter(self, article: str, prix_unitaire: int, quantite: int = 1) -> None:
        if prix_unitaire < 0 or quantite <= 0:
            raise ValueError("prix négatif ou quantité nulle")
        _, deja = self._lignes.get(article, (prix_unitaire, 0))
        self._lignes[article] = (prix_unitaire, deja + quantite)

    def sous_total(self) -> int:
        return sum(prix * quantite for prix, quantite in self._lignes.values())

    def appliquer_code(self, code: str) -> None:
        code = code.upper()
        if code not in CODES:
            raise ValueError(f"code inconnu : {code}")
        if self._code is not None:
            raise ValueError("un seul code par panier")
        if code == "MOINS5" and self.sous_total() < SEUIL_MOINS5:
            raise ValueError("MOINS5 exige un panier d'au moins 30 €")
        self._code = code

    def total(self) -> int:
        sous_total = self.sous_total()
        remise = CODES[self._code](sous_total) if self._code else 0
        return max(sous_total - remise, 0)
