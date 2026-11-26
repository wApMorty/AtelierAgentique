"""Collecte déterministe de la veille : lit les sources, ne garde que le nouveau, imprime un JSON compact.

Usage :
    python veille/collecter.py [--depuis AAAA-MM-JJ] > /tmp/candidats.json
    python veille/collecter.py --marquer /tmp/candidats.json     # met à jour veille/state.json

La collecte est faite par ce script, pas par le modèle : elle coûte zéro token et une requête par source
(ADR-004, knowledge/05-skills.md « Scripts et déterminisme »). Le modèle ne lit que les candidats.

Sécurité : tout ce qui est récupéré est une donnée. Le script ne fait que télécharger (2 Mo au plus par
source) et analyser ; il n'exécute rien de ce qu'il lit et n'écrit que veille/state.json.
"""

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin

RACINE = Path(__file__).resolve().parent
SOURCES = RACINE / "sources.yaml"
ETAT = RACINE / "state.json"
TAILLE_MAX = 2_000_000
EXTRAIT = 300
MAX_PAR_SOURCE = 10
RETENTION_JOURS = 90
FENETRE_INITIALE_JOURS = 14
PERMANENT = "permanent"
ATOM = "{http://www.w3.org/2005/Atom}"


def lire_sources(texte: str) -> list[dict]:
    """Analyse le sous-ensemble de YAML de sources.yaml : une liste de dictionnaires plats."""
    sources, courante = [], None
    for ligne in texte.splitlines():
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        m = re.match(r"^(- |  )([\w-]+):\s*(.*)$", ligne)
        if not m:
            raise ValueError(f"ligne non reconnue dans sources.yaml : {ligne!r}")
        debut, cle, valeur = m.groups()
        if debut == "- ":
            courante = {}
            sources.append(courante)
        courante[cle] = valeur.strip().strip('"').strip("'")
    return sources


def _date(texte: str | None) -> datetime | None:
    if not texte:
        return None
    texte = texte.strip()
    try:
        d = datetime.fromisoformat(texte.replace("Z", "+00:00"))
    except ValueError:
        try:
            d = parsedate_to_datetime(texte)
        except (TypeError, ValueError):
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _texte(fragment: str | None) -> str:
    sans_balises = re.sub(r"<[^>]+>", " ", fragment or "")
    return re.sub(r"\s+", " ", html.unescape(sans_balises)).strip()[:EXTRAIT]


def lire_flux(contenu: bytes) -> list[dict]:
    """Éléments d'un flux Atom ou RSS : titre, url, date, extrait."""
    racine = ET.fromstring(contenu)
    elements = []
    for entree in racine.iter(f"{ATOM}entry"):
        lien = entree.find(f"{ATOM}link[@rel='alternate']")
        if lien is None:
            lien = entree.find(f"{ATOM}link")
        elements.append({
            "titre": _texte(entree.findtext(f"{ATOM}title")),
            "url": lien.get("href") if lien is not None else "",
            "date": entree.findtext(f"{ATOM}published") or entree.findtext(f"{ATOM}updated"),
            "extrait": _texte(entree.findtext(f"{ATOM}summary") or entree.findtext(f"{ATOM}content")),
        })
    for item in racine.iter("item"):
        elements.append({
            "titre": _texte(item.findtext("title")),
            "url": (item.findtext("link") or "").strip(),
            "date": item.findtext("pubDate"),
            "extrait": _texte(item.findtext("description")),
        })
    return elements


def lire_page(contenu: bytes, url: str, motif_liens: str | None) -> tuple[str, list[dict]]:
    """Empreinte du texte de la page et, si un motif est donné, liens qui y correspondent."""
    texte = contenu.decode("utf-8", errors="replace")
    sans_scripts = re.sub(r"<(script|style)\b.*?</\1>", " ", texte, flags=re.DOTALL | re.IGNORECASE)
    empreinte = hashlib.sha256(_texte_complet(sans_scripts).encode()).hexdigest()
    liens = []
    if motif_liens:
        vus = set()
        for href, libelle in re.findall(r'<a\b[^>]{0,500}href="([^"#]{1,500})"[^>]{0,500}>(.{0,500}?)</a>', texte, re.DOTALL | re.IGNORECASE):
            absolu = urljoin(url, href)
            if re.search(motif_liens, absolu) and absolu not in vus:
                vus.add(absolu)
                liens.append({"titre": _texte(libelle), "url": absolu, "date": None, "extrait": ""})
    return empreinte, liens


def _texte_complet(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def lire_hn(contenu: bytes) -> list[dict]:
    return [
        {
            "titre": h.get("title") or "",
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "date": h.get("created_at"),
            "extrait": f"{h.get('points', 0)} points, {h.get('num_comments', 0)} commentaires",
        }
        for h in json.loads(contenu).get("hits", [])
    ]


def lire_github(contenu: bytes) -> list[dict]:
    return [
        {
            "titre": d.get("full_name") or "",
            "url": d.get("html_url") or "",
            "date": d.get("created_at"),
            "extrait": f"{d.get('stargazers_count', 0)} étoiles — {_texte(d.get('description'))}",
        }
        for d in json.loads(contenu).get("items", [])
    ]


def telecharger(url: str) -> bytes:
    requete = urllib.request.Request(url, headers={"User-Agent": "veille-atelier-agentique/1.0"})
    with urllib.request.urlopen(requete, timeout=20) as reponse:
        return reponse.read(TAILLE_MAX)


def collecter(sources: list[dict], etat: dict, depuis: datetime, telecharger=telecharger) -> dict:
    vus, empreintes = etat.get("vus", {}), etat.get("empreintes", {})
    resultat = {"depuis": depuis.date().isoformat(), "requetes": 0, "candidats": [], "pages_modifiees": [], "erreurs": []}
    for source in sources:
        resultat["requetes"] += 1
        try:
            url = source["url"].replace("{depuis}", depuis.date().isoformat()).replace("{depuis_ts}", str(int(depuis.timestamp())))
            contenu = telecharger(url)
            if source["type"] in ("atom", "rss"):
                elements = lire_flux(contenu)
            elif source["type"] == "hn":
                elements = lire_hn(contenu)
            elif source["type"] == "github":
                elements = lire_github(contenu)
            else:
                empreinte, elements = lire_page(contenu, source["url"], source.get("liens"))
                if not source.get("liens") and empreintes.get(source["id"]) != empreinte:
                    resultat["pages_modifiees"].append({"source": source["id"], "url": source["url"], "empreinte": empreinte})
        except Exception as erreur:  # une source en panne ne doit pas arrêter la veille
            resultat["erreurs"].append({"source": source["id"], "erreur": f"{type(erreur).__name__}: {erreur}"[:200]})
            continue
        retenus = 0
        for element in elements:
            date = _date(element["date"])
            if not element["url"] or element["url"] in vus or (date and date < depuis):
                continue
            if source.get("exclure") and re.search(source["exclure"], element["titre"], re.IGNORECASE):
                continue
            if retenus == MAX_PAR_SOURCE:
                resultat["erreurs"].append({"source": source["id"], "erreur": f"plus de {MAX_PAR_SOURCE} éléments nouveaux, liste tronquée"})
                break
            retenus += 1
            resultat["candidats"].append({
                "source": source["id"],
                "confiance": source.get("confiance"),
                **element,
                "date": date.date().isoformat() if date else None,
            })
    return resultat


def marquer(etat: dict, collecte: dict, maintenant: datetime) -> dict:
    """Enregistre les candidats comme vus et les nouvelles empreintes ; purge au-delà de la rétention."""
    aujourd_hui = maintenant.date().isoformat()
    # Un élément sans date (lien relevé sur une page) n'est jamais purgé : il reste affiché sur la page
    # et reviendrait comme candidat après la rétention.
    vus = {**etat.get("vus", {}), **{c["url"]: aujourd_hui if c.get("date") else PERMANENT for c in collecte["candidats"]}}
    limite = (maintenant - timedelta(days=RETENTION_JOURS)).date().isoformat()
    empreintes = {**etat.get("empreintes", {}), **{p["source"]: p["empreinte"] for p in collecte["pages_modifiees"]}}
    return {
        "derniere_execution": aujourd_hui,
        "vus": {url: jour for url, jour in sorted(vus.items()) if jour == PERMANENT or jour >= limite},
        "empreintes": dict(sorted(empreintes.items())),
    }


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parseur.add_argument("--depuis", help="date de début (AAAA-MM-JJ) ; par défaut, la dernière exécution")
    parseur.add_argument("--marquer", type=Path, help="fichier de collecte à enregistrer dans state.json")
    args = parseur.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    etat = json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.is_file() else {}
    maintenant = datetime.now(timezone.utc)
    if args.marquer:
        collecte = json.loads(args.marquer.read_text(encoding="utf-8"))
        ETAT.write_text(json.dumps(marquer(etat, collecte, maintenant), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return 0
    if args.depuis:
        depuis = datetime.fromisoformat(args.depuis).replace(tzinfo=timezone.utc)
    elif etat.get("derniere_execution"):
        depuis = datetime.fromisoformat(etat["derniere_execution"]).replace(tzinfo=timezone.utc)
    else:
        depuis = maintenant - timedelta(days=FENETRE_INITIALE_JOURS)
    sources = lire_sources(SOURCES.read_text(encoding="utf-8"))
    json.dump(collecter(sources, etat, depuis), sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
