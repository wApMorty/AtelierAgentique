"""Critères de réussite du lab 02.

Lancement sur votre hook :     python -m unittest discover -s labs/02-hook-garde-fou/tests
Lancement sur la solution :    LAB02_HOOK=labs/02-hook-garde-fou/solution/hook.py python -m unittest discover -s labs/02-hook-garde-fou/tests
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
HOOK = Path(os.environ.get("LAB02_HOOK") or LAB / "depart" / "hook.py").resolve()


class HookMigrations(unittest.TestCase):
    def setUp(self):
        self.projet = tempfile.TemporaryDirectory()
        self.racine = Path(self.projet.name)
        (self.racine / "migrations").mkdir()
        (self.racine / "migrations" / "0001_initiale.sql").write_text("CREATE TABLE t (id int);", encoding="utf-8")
        (self.racine / "src").mkdir()
        (self.racine / "src" / "app.py").write_text("x = 1", encoding="utf-8")

    def tearDown(self):
        self.projet.cleanup()

    def appel(self, outil: str, chemin: str, absolu: bool = True):
        fichier = str(self.racine / chemin) if absolu else chemin
        entree = {
            "hook_event_name": "PreToolUse",
            "tool_name": outil,
            "tool_input": {"file_path": fichier, "content": "x", "old_string": "a", "new_string": "b"},
            "cwd": str(self.racine),
        }
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(entree),
            capture_output=True,
            text=True,
            cwd=self.racine,
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.racine)},
        )

    def test_bloque_la_modification_d_une_migration_existante(self):
        for outil in ("Edit", "Write", "MultiEdit"):
            with self.subTest(outil=outil):
                r = self.appel(outil, "migrations/0001_initiale.sql")
                self.assertEqual(r.returncode, 2)
                self.assertTrue(r.stderr.strip(), "la raison du blocage doit être donnée sur stderr")

    def test_bloque_aussi_avec_un_chemin_relatif(self):
        self.assertEqual(self.appel("Edit", "migrations/0001_initiale.sql", absolu=False).returncode, 2)

    def test_autorise_une_nouvelle_migration(self):
        self.assertEqual(self.appel("Write", "migrations/0002_ajout.sql").returncode, 0)

    def test_autorise_le_reste_du_projet(self):
        self.assertEqual(self.appel("Edit", "src/app.py").returncode, 0)

    def test_ne_se_laisse_pas_tromper_par_un_nom_voisin(self):
        (self.racine / "src" / "migrations_utils.py").write_text("y = 2", encoding="utf-8")
        self.assertEqual(self.appel("Edit", "src/migrations_utils.py").returncode, 0)

    def test_message_utile_a_l_agent(self):
        r = self.appel("Edit", "migrations/0001_initiale.sql")
        self.assertIn("migration", r.stderr.lower())


if __name__ == "__main__":
    unittest.main()
