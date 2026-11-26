import unittest

from panier import Panier


class TestPanier(unittest.TestCase):
    def test_total_vide(self):
        self.assertEqual(Panier().total(), 0)

    def test_total_cumule_les_quantites(self):
        p = Panier()
        p.ajouter("livre", 1500, 2)
        p.ajouter("livre", 1500)
        p.ajouter("stylo", 250)
        self.assertEqual(p.total(), 4750)

    def test_refuse_quantite_nulle(self):
        with self.assertRaises(ValueError):
            Panier().ajouter("livre", 1500, 0)


if __name__ == "__main__":
    unittest.main()
