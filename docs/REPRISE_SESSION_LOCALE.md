# Reprise en local : mise en ligne de michelgallone.ch

Note laissée par la session cloud pour la session Claude Code locale (Mac, avec Chrome).

## Où en est le site

- Branche : `claude/affectionate-euler-tp4710`
- Trois pages en français : `site/fr/index.html` (accueil), `site/fr/parcours.html` (parcours complet), `site/fr/contact.html` (carte de visite, vCard, QR code).
- `site/index.html` redirige vers `site/fr/`. La version anglaise ira dans `site/en/`.
- Journal de bord : `docs/journal/journal_de_bord.html` → `node docs/build_pdf.js` régénère les captures et `docs/Journal_de_bord_site_Michel_Gallone.pdf`. Chaque modification du site ajoute une étape (la dernière est la 47) avant la section « Annexe ».
- vCard et QR code : coordonnées en haut de `tools/make_contact.py`, puis `tools/.venv/bin/python tools/make_contact.py`.

## Déjà fait pour la mise en ligne (étape 48, en cours)

- Adresse définitive confirmée : `https://michelgallone.ch`.
- Image de partage `site/assets/img/og-image.jpg` (1200 × 630).
- Sur les trois pages : `link rel="canonical"`, `og:url`, `og:image` en adresse complète, `twitter:card`.
- Adresses prévues : `/fr/`, `/fr/parcours`, `/fr/contact` (sans `.html`).

## Reste à faire

1. Créer `server/` sur le modèle de `sowattmusic/route108-site/server/` :
   - `.htaccess` : `Options -Indexes`, `ErrorDocument 404 /404.html`, www → sans www et http → https vers `https://michelgallone.ch`, `/` → `/fr/` (302, pour la future version anglaise), `/fr/index.html` → `/fr/`, adresses courtes (`/fr/contact` → `contact.html`), `AddType text/vcard .vcf`, en-tête `X-Robots-Tag: noindex` et `Cache-Control: private, no-store` sur les `.vcf`, compression et cache comme Route 108.
   - `robots.txt` (avec `Sitemap: https://michelgallone.ch/sitemap.xml`), `sitemap.xml` (les trois pages), `404.html` au look sombre du site.
2. Créer `build.sh` qui fabrique `deploy/` : contenu de `site/` + fichiers de `server/` (`.htaccess` compris). Ajouter `deploy/` à `.gitignore`.
3. Téléverser le contenu de `deploy/` avec Chrome dans le gestionnaire de fichiers N0C, dossier `michelgallone.ch/` :
   https://nodels65-eu.n0c.com:4443/fb/cpjhfswt/files/michelgallone.ch/
   (Michel est connecté dans son Chrome ; ne jamais demander ni enregistrer de mot de passe.) Vérifier d'abord ce que contient déjà le dossier avant de remplacer quoi que ce soit.
4. Tester en ligne : les trois pages, `/fr/contact#qr`, le téléchargement de la vCard sur iPhone et Android, la redirection http → https, une page 404, l'aperçu de partage (LinkedIn Post Inspector).
5. Ajouter l'étape 48 « Mise en ligne sur michelgallone.ch » au journal, régénérer le PDF, commit et push.

## Points encore ouverts avec Michel

- CV PDF téléchargeable (`site/assets/CV_Michel_Gallone.pdf`) : à mettre à jour (second titre, contact@michelgallone.ch, missions) pour correspondre au site.
- Lien LinkedIn incomplet sur linkin.bio/mg (il manque `/in/`).
- Media One Group et Loreto1 Trading SA : dates et rôles à préciser si Michel le souhaite.
- Version anglaise.
