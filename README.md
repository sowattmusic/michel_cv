# michel_cv

Le CV de Michel Gallone : directeur technique audiovisuel, réalisateur TV & radio, ingénieur du son.

## Contenu

| Chemin | Description |
| --- | --- |
| `renders/<métier>/` | Une variante du CV par métier : source HTML + PDF |
| `renders/ingeson/CV_Michel_Gallone_ingeson.pdf` | CV ingénieur du son / directeur technique, 2 pages A4 |
| `renders/ingeson/CV_Michel_Gallone_ingeson.html` | Source de ce CV (HTML/CSS) |
| `renders/ingeson_photo/` | Même CV avec portrait en fondu dans l'en-tête (`portrait.jpg`, recadré de `sources/photos/DSC_8780.jpg`) |
| `renders/chefdeprojet/` | CV orienté chef de projet (sans photo) : M Le Media, Sully Sound et Digital Media Partners réécrits côté management |
| `renders/chefdeprojet_photo/` | Même CV chef de projet, avec le portrait en fondu dans l'en-tête |
| `site/` | CV en ligne de Michel, orienté gestion de projet, visibilité et marketing. Ouvrir `site/index.html` (redirige vers `site/fr/`). Pages : `site/fr/index.html` (accueil), `site/fr/parcours.html` (parcours complet), `site/fr/contact.html` (carte de visite avec vCard et QR code). Version anglaise à venir dans `site/en/` |
| `docs/Journal_de_bord_site_Michel_Gallone.pdf` | Journal de bord du site : sources, choix, tests, points à valider |
| `docs/journal/` | Source HTML du journal et captures d'écran ; `node docs/build_pdf.js` régénère captures et PDF |
| `tools/make_contact.py` | Crée la vCard (`site/assets/contact/Michel_Gallone.vcf`) et le QR code de la page Contact à partir des coordonnées écrites en haut du script |
| `sources/web/` | Données collectées en ligne : interview Headliner, linkin.bio, API Discogs |
| `sources/photos/` | Photos originales de Michel |
| `sources/tech_multimedia_Gallone.pdf` | Ancien CV, utilisé comme source |
| `conversation/conversation.md` | Conversation avec Claude, version lisible |
| `conversation/export/` | Export brut de la session Claude Code (transcription, métadonnées) |

## Régénérer le PDF

Depuis le sous-dossier de la variante (ex. `renders/ingeson`) :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV_Michel_Gallone_ingeson.pdf "file://$PWD/CV_Michel_Gallone_ingeson.html"
```
