"""Tests d'acceptation du lab 01, exécutés par verifier.py contre le code de l'apprenant.

Ils restent hors du dépôt de l'apprenant : un agent ne doit pas pouvoir modifier le contrôle qui le juge
(knowledge/09-verification-et-evaluation.md).
"""

import unittest

from panier import Panier


def panier(total_centimes: int) -> Panier:
    p = Panier()
    p.ajouter("article", total_centimes)
    return p


class CodesPromo(unittest.TestCase):
    def test_pourcent10(self):
        p = panier(5000)
        p.appliquer_code("POURCENT10")
        self.assertEqual(p.total(), 4500)

    def test_pourcent10_arrondi_au_centime_inferieur(self):
        p = panier(999)
        p.appliquer_code("POURCENT10")
        self.assertEqual(p.total(), 900)  # 999 - 99,9 → remise arrondie à 99 centimes

    def test_moins5_a_partir_de_30_euros(self):
        p = panier(3000)
        p.appliquer_code("MOINS5")
        self.assertEqual(p.total(), 2500)

    def test_moins5_refuse_sous_30_euros(self):
        with self.assertRaises(ValueError):
            panier(2999).appliquer_code("MOINS5")

    def test_code_inconnu(self):
        with self.assertRaises(ValueError):
            panier(5000).appliquer_code("GRATUIT")

    def test_codes_non_cumulables(self):
        p = panier(5000)
        p.appliquer_code("POURCENT10")
        with self.assertRaises(ValueError):
            p.appliquer_code("MOINS5")

    def test_insensible_a_la_casse(self):
        p = panier(5000)
        p.appliquer_code("pourcent10")
        self.assertEqual(p.total(), 4500)

    def test_remise_recalculee_apres_ajout(self):
        p = panier(5000)
        p.appliquer_code("POURCENT10")
        p.ajouter("autre", 1000)
        self.assertEqual(p.total(), 5400)


if __name__ == "__main__":
    unittest.main()
