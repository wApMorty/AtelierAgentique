// Critères de réussite automatiques du lab 03.
// Sur votre skill :      node --test labs/03-conception-skill/tests/
// Sur la solution :      LAB03_SKILL=labs/03-conception-skill/solution/composant-angular node --test labs/03-conception-skill/tests/
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const racine = resolve(ici, '..', '..', '..');
const skill = resolve(process.env.LAB03_SKILL ?? join(ici, '..', 'composant-angular'));
const fixtures = join(ici, 'fixtures');

test('le SKILL.md respecte le format Agent Skills du dépôt', () => {
  const r = spawnSync('python', [join(racine, '.github', 'scripts', 'verifier_skills.py'), join(skill, 'SKILL.md')], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stdout + r.stderr);
});

test('le SKILL.md reste court et renvoie vers ses références', () => {
  const texte = readFileSync(join(skill, 'SKILL.md'), 'utf8');
  assert.ok(texte.split('\n').length <= 200, 'SKILL.md de plus de 200 lignes');
  assert.match(texte, /references\//);
  assert.ok(existsSync(join(skill, 'references')), 'dossier references/ absent');
});

test('le script accepte un composant conforme', async () => {
  const { verifierComposant } = await import(pathToFileURL(join(skill, 'scripts', 'verifier.mjs')).href);
  assert.deepEqual(verifierComposant(join(fixtures, 'conforme', 'carte-produit')), []);
});

test('le script détecte chaque écart du composant non conforme', async () => {
  const { verifierComposant } = await import(pathToFileURL(join(skill, 'scripts', 'verifier.mjs')).href);
  const ecarts = verifierComposant(join(fixtures, 'non-conforme', 'ancien')).join('\n');
  for (const attendu of [/spec\.ts/, /OnPush/, /@Input|input\(\)/, /NgModule|autonome/, /sélecteur/]) {
    assert.match(ecarts, attendu);
  }
});

test('le script s\'utilise en ligne de commande avec un code de sortie', () => {
  const verifier = join(skill, 'scripts', 'verifier.mjs');
  execFileSync('node', [verifier, join(fixtures, 'conforme', 'carte-produit')]);
  const r = spawnSync('node', [verifier, join(fixtures, 'non-conforme', 'ancien')]);
  assert.equal(r.status, 1);
});
