# michel_cv

Le CV de Michel Gallone : directeur technique audiovisuel, réalisateur TV & radio, ingénieur du son.

## Contenu

| Chemin | Description |
| --- | --- |
| `renders/CV/<métier>/` | Une variante du CV par métier : source HTML + PDF |
| `renders/lettres_postulations/<employeur>/` | Une lettre de motivation par candidature : HTML, PDF et Word |
| `renders/CV/ingeson/CV_Michel_Gallone_ingeson.pdf` | CV ingénieur du son / directeur technique, 2 pages A4 |
| `renders/CV/ingeson/CV_Michel_Gallone_ingeson.html` | Source de ce CV (HTML/CSS) |
| `renders/CV/ingeson_photo/` | Même CV avec portrait en fondu dans l'en-tête (`portrait.jpg`, recadré de `sources/photos/DSC_8780.jpg`) |
| `renders/CV/dirtech_photo/` | CV directeur technique avec portrait : comme `ingeson_photo`, mais Sowatt Music décrit côté installations son / vidéo et captations |
| `renders/CV/chefdeprojet/` | CV orienté chef de projet (sans photo) : M Le Media, Sully Sound et Digital Media Partners réécrits côté management |
| `renders/CV/chefdeprojet_photo/` | Même CV chef de projet, avec le portrait en fondu dans l'en-tête |
| `renders/CV/assistantadmin_photo/` | CV assistant administratif, tiré du CV chef de projet : expériences réécrites côté secrétariat et administration, nouveau portrait (`portrait.jpg`, recadré de `sources/photos/Michel_01.jpg`) |
| `renders/lettres_postulations/lettre_orp_echallens/` | Lettre de motivation pour le poste d'assistant administratif à 80 % chez Pierre Mivelaz Electricité SA, Poliez-Pittet (annonce Job-Room réf. 00002548673) ; lettre adressée à l'ORP d'Echallens, qui mène la présélection : HTML, PDF, Word |
| `renders/lettres_postulations/lettre_dorier/` | Lettre de motivation pour le poste de technicien audiovisuel, spécialiste son, chez Dorier Group, Genève (adressée aux RH à Satigny) ; profil technique son, avec le CV ingénieur du son : HTML, PDF, Word |
| `renders/lettres_postulations/lettre_arsenic/` | Lettre de motivation pour le poste de directeur·rice·x technique à l'Arsenic, Lausanne (HTML + PDF, même charte que les CV, et version Word `.docx` modifiable) |
| `renders/lettres_postulations/lettre_avdc/` | Lettre de motivation pour le poste de chargé·e·x de production et de communication à l'AVDC (association vaudoise de danse contemporaine), Lausanne : profil organisation et gestion de projet (HTML, PDF, Word) |
| `site/` | CV en ligne de Michel, orienté gestion de projet, visibilité et marketing. Ouvrir `site/index.html` (redirige vers `site/fr/`). Pages : `site/fr/index.html` (accueil), `site/fr/parcours.html` (parcours complet), `site/fr/contact.html` (carte de visite avec vCard et QR code). Version anglaise dans `site/en/`, générée à partir des pages françaises par `tools/make_en.py` |
| `docs/Journal_de_bord_site_Michel_Gallone.pdf` | Journal de bord du site : sources, choix, tests, points à valider |
| `docs/journal/` | Source HTML du journal et captures d'écran ; `node docs/build_pdf.js` régénère captures et PDF |
| `tools/make_en.py` | Fabrique `site/en/` (traduction anglaise) à partir de `site/fr/` et active le sélecteur FR / EN et les balises hreflang. À relancer après chaque modification d'une page française ; il s'arrête et nomme la phrase si un texte français a changé et n'a plus de traduction |
| `tools/make_contact.py` | Crée la vCard (`site/assets/contact/Michel_Gallone.vcf`) et le QR code de la page Contact à partir des coordonnées écrites en haut du script |
| `sources/web/` | Données collectées en ligne : interview Headliner, linkin.bio, API Discogs |
| `sources/photos/` | Photos originales de Michel |
| `sources/tech_multimedia_Gallone.pdf` | Ancien CV, utilisé comme source |
| `conversation/conversation.md` | Conversation avec Claude, version lisible |
| `conversation/export/` | Export brut de la session Claude Code (transcription, métadonnées) |

## Régénérer le PDF

Depuis le sous-dossier de la variante (ex. `renders/CV/ingeson`) :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV_Michel_Gallone_ingeson.pdf "file://$PWD/CV_Michel_Gallone_ingeson.html"
```
