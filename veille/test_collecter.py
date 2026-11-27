"""Tests de veille/collecter.py, sans réseau. Lancement : python -m unittest veille/test_collecter.py"""

import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collecter  # noqa: E402

ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Nouveau</title><link rel="alternate" href="https://ex.org/nouveau"/><updated>2026-11-20T10:00:00Z</updated><summary>&lt;p&gt;Texte&lt;/p&gt;</summary></entry>
<entry><title>Ancien</title><link href="https://ex.org/ancien"/><updated>2026-10-01T10:00:00Z</updated></entry>
<entry><title>v1.0-alpha.1</title><link href="https://ex.org/alpha"/><updated>2026-11-21T10:00:00Z</updated></entry>
</feed>"""
RSS = b"""<rss><channel><item><title>Billet</title><link>https://ex.org/billet</link><pubDate>Mon, 23 Nov 2026 08:00:00 GMT</pubDate><description>Resume</description></item></channel></rss>"""
PAGE = b"""<html><body><a href="/blog/un-article/">Un article</a><a href="/a-propos">A propos</a><script>x()</script></body></html>"""
DEPUIS = datetime(2026, 11, 13, tzinfo=timezone.utc)


class Collecter(unittest.TestCase):
    def test_lire_sources(self):
        sources = collecter.lire_sources("# commentaire\n- id: a\n  url: https://ex.org\n  type: atom\n\n- id: b\n  type: page\n")
        self.assertEqual([s["id"] for s in sources], ["a", "b"])
        self.assertEqual(sources[0]["url"], "https://ex.org")

    def test_sources_du_depot(self):
        sources = collecter.lire_sources(collecter.SOURCES.read_text(encoding="utf-8"))
        self.assertLessEqual(len(sources), 25, "ADR-004 : 25 sources au plus")
        for s in sources:
            self.assertTrue({"id", "url", "type", "confiance", "justification"} <= s.keys(), s.get("id"))
            self.assertIn(s["confiance"], {"officiel", "pratique", "emergent"})

    def test_flux_fenetre_vus_et_exclusion(self):
        pages = {"https://f/atom": ATOM, "https://f/rss": RSS}
        sources = [
            {"id": "atom", "url": "https://f/atom", "type": "atom", "exclure": "alpha"},
            {"id": "rss", "url": "https://f/rss", "type": "rss"},
        ]
        etat = {"vus": {"https://ex.org/billet": "2026-11-23"}}
        resultat = collecter.collecter(sources, etat, DEPUIS, telecharger=pages.__getitem__)
        self.assertEqual([c["url"] for c in resultat["candidats"]], ["https://ex.org/nouveau"])
        self.assertEqual(resultat["candidats"][0]["extrait"], "Texte")
        self.assertEqual(resultat["requetes"], 2)

    def test_page_liens_et_empreinte(self):
        source = {"id": "blog", "url": "https://ex.org/blog", "type": "page", "liens": "/blog/[a-z0-9-]+/?$"}
        resultat = collecter.collecter([source], {}, DEPUIS, telecharger=lambda url: PAGE)
        self.assertEqual([c["url"] for c in resultat["candidats"]], ["https://ex.org/blog/un-article/"])
        sans_liens = {"id": "chg", "url": "https://ex.org/chg", "type": "page"}
        resultat = collecter.collecter([sans_liens], {}, DEPUIS, telecharger=lambda url: PAGE)
        self.assertEqual(len(resultat["pages_modifiees"]), 1)
        etat = collecter.marquer({}, resultat, DEPUIS)
        resultat = collecter.collecter([sans_liens], etat, DEPUIS, telecharger=lambda url: PAGE)
        self.assertEqual(resultat["pages_modifiees"], [])

    def test_api_github_versions_et_commits(self):
        versions = json.dumps([
            {"tag_name": "v2", "name": "v2", "html_url": "https://g/v2", "published_at": "2026-11-20T00:00:00Z", "prerelease": False, "body": "Nouveau"},
            {"tag_name": "v3-alpha", "html_url": "https://g/v3", "published_at": "2026-11-21T00:00:00Z", "prerelease": True},
        ]).encode()
        commits = json.dumps([
            {"html_url": "https://g/c1", "commit": {"message": "Ajoute la gouvernance\n\nDétail", "committer": {"date": "2026-11-22T00:00:00Z"}}},
        ]).encode()
        pages = {"https://api/versions": versions, "https://api/commits": commits}
        sources = [{"id": "v", "url": "https://api/versions", "type": "github-api"}, {"id": "c", "url": "https://api/commits", "type": "github-api"}]
        resultat = collecter.collecter(sources, {}, DEPUIS, telecharger=pages.__getitem__)
        self.assertEqual([(c["titre"], c["url"]) for c in resultat["candidats"]], [("v2", "https://g/v2"), ("Ajoute la gouvernance", "https://g/c1")])

    def test_erreur_isolee(self):
        def panne(url):
            raise OSError("hors ligne")
        resultat = collecter.collecter([{"id": "x", "url": "https://x", "type": "rss"}], {}, DEPUIS, telecharger=panne)
        self.assertEqual(resultat["erreurs"][0]["source"], "x")

    def test_marquer_purge(self):
        etat = {"vus": {"https://vieux": "2026-01-01"}}
        collecte = {"candidats": [{"url": "https://neuf", "date": "2026-11-26"}, {"url": "https://lien-de-page", "date": None}], "pages_modifiees": []}
        nouvel_etat = collecter.marquer(etat, collecte, datetime(2026, 11, 27, tzinfo=timezone.utc))
        self.assertEqual(nouvel_etat["vus"], {"https://lien-de-page": "permanent", "https://neuf": "2026-11-27"})
        plus_tard = collecter.marquer(nouvel_etat, {"candidats": [], "pages_modifiees": []}, datetime(2027, 6, 1, tzinfo=timezone.utc))
        self.assertEqual(plus_tard["vus"], {"https://lien-de-page": "permanent"})
        self.assertEqual(nouvel_etat["derniere_execution"], "2026-11-27")


if __name__ == "__main__":
    unittest.main()
