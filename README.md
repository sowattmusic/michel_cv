# michel_cv

Le CV de Michel Gallone : directeur technique audiovisuel, réalisateur TV & radio, ingénieur du son.

## Contenu

| Chemin | Description |
| --- | --- |
| `renders/<métier>/` | Une variante du CV par métier : source HTML + PDF |
| `renders/ingeson/CV_Michel_Gallone_ingeson.pdf` | CV ingénieur du son / directeur technique, 2 pages A4 |
| `renders/ingeson/CV_Michel_Gallone_ingeson.html` | Source de ce CV (HTML/CSS) |
| `renders/ingeson_photo/` | Même CV avec portrait en fondu dans l'en-tête (`portrait.jpg`, recadré de `sources/photos/DSC_8780.jpg`) |
| `sources/photos/` | Photos originales de Michel |
| `sources/tech_multimedia_Gallone.pdf` | Ancien CV, utilisé comme source |
| `conversation/conversation.md` | Conversation avec Claude, version lisible |
| `conversation/export/` | Export brut de la session Claude Code (transcription, métadonnées) |

## Régénérer le PDF

Depuis le sous-dossier de la variante (ex. `renders/ingeson`) :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV_Michel_Gallone_ingeson.pdf "file://$PWD/CV_Michel_Gallone_ingeson.html"
```
