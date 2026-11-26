// Vérifie qu'un dossier de composant respecte les conventions de references/conventions.md.
// Usage : node verifier.mjs <dossier du composant>   — code 1 et liste des écarts si non conforme.
import { existsSync, readFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export function verifierComposant(dossier) {
  const nom = basename(dossier);
  const source = join(dossier, `${nom}.ts`);
  const ecarts = [];
  for (const fichier of [`${nom}.ts`, `${nom}.html`, `${nom}.spec.ts`]) {
    if (!existsSync(join(dossier, fichier))) ecarts.push(`fichier manquant : ${fichier}`);
  }
  if (!existsSync(source)) return ecarts;
  const code = readFileSync(source, 'utf8');
  if (!code.includes(`selector: 'app-${nom}'`)) ecarts.push(`sélecteur attendu : app-${nom}`);
  if (!/ChangeDetectionStrategy\.OnPush/.test(code)) ecarts.push('détection de changements OnPush absente');
  if (/standalone:\s*false|NgModule/.test(code)) ecarts.push('composant non autonome ou NgModule');
  if (/@(Input|Output)\s*\(/.test(code)) ecarts.push('décorateur @Input ou @Output : utiliser input() et output()');
  return ecarts;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const ecarts = verifierComposant(process.argv[2] ?? '.');
  for (const e of ecarts) console.error(`- ${e}`);
  console.log(ecarts.length ? `${ecarts.length} écart(s)` : 'Composant conforme');
  process.exit(ecarts.length ? 1 : 0);
}
