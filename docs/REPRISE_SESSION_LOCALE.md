# Reprise en local : mise en ligne de michelgallone.ch

Note laissée par la session cloud pour la session Claude Code locale (Mac, avec Chrome).

## Où en est le site

- Branche : `main` (la branche de travail a été fusionnée puis supprimée)
- Trois pages en français : `site/fr/index.html` (accueil), `site/fr/parcours.html` (parcours complet), `site/fr/contact.html` (carte de visite, vCard, QR code).
- `site/index.html` redirige vers `site/fr/`. La version anglaise ira dans `site/en/`.
- Journal de bord : `docs/journal/journal_de_bord.html` → `node docs/build_pdf.js` régénère les captures et `docs/Journal_de_bord_site_Michel_Gallone.pdf`. Chaque modification du site ajoute une étape (la dernière est la 54) avant la section « Annexe ».
- vCard et QR code : coordonnées en haut de `tools/make_contact.py`, puis `tools/.venv/bin/python tools/make_contact.py`.

## Mise en ligne : faite (étapes 48 et 49 du journal)

- Le site est en ligne sur https://michelgallone.ch (gestionnaire de fichiers N0C, dossier `michelgallone.ch/`).
- `server/` contient `.htaccess`, `robots.txt`, `sitemap.xml` et `404.html`.
- `./build.sh` fabrique `deploy/` (ignoré par git) à partir de `site/` et `server/`.
- Si `site/assets/css/style.css` change, augmenter le numéro `?v=` du lien vers la feuille de style dans les trois pages (le serveur la garde une semaine en cache).
- Ordre de téléversement : **la feuille de style d'abord, les pages ensuite.** Sinon un visiteur peut charger la nouvelle page pendant que l'ancienne feuille est encore sur le serveur, et la garder une semaine sous le nouveau numéro (arrivé le 29.10.2026 avec `?v=4`, corrigé par `?v=5`).
- Pour mettre à jour : `./build.sh`, puis téléverser les fichiers modifiés de `deploy/` avec Chrome dans
  https://nodels65-eu.n0c.com:4443/fb/cpjhfswt/files/michelgallone.ch/
  (Michel est connecté dans son Chrome ; ne jamais demander ni enregistrer de mot de passe.)
- Vérifiés en ligne : les trois pages, `/fr/contact#qr`, les redirections http/www/racine, la page 404, les en-têtes de la vCard.
- Reste à vérifier : enregistrement de la vCard sur iPhone et Android, aperçu de partage (LinkedIn Post Inspector).
- Le PDF du journal se régénère avec `node docs/build_pdf.js` ; il faut Playwright (`require('playwright')`), qui n'est pas installé dans le projet.

## Points encore ouverts avec Michel

- CV PDF téléchargeable (`site/assets/CV_Michel_Gallone.pdf`) : à mettre à jour (second titre, contact@michelgallone.ch, missions) pour correspondre au site.
- Lien LinkedIn incomplet sur linkin.bio/mg (il manque `/in/`).
- Media One Group et Loreto1 Trading SA : dates et rôles à préciser si Michel le souhaite.
- Version anglaise.
