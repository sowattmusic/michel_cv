# michel_cv

Le CV de Michel Gallone : directeur technique audiovisuel, réalisateur TV & radio, ingénieur du son.

## Contenu

| Chemin | Description |
| --- | --- |
| `CV_Michel_Gallone_2026.pdf` | CV final, 2 pages A4, prêt à imprimer |
| `CV_Michel_Gallone_2026.html` | Source du CV (HTML/CSS), à modifier pour faire évoluer le PDF |
| `sources/tech_multimedia_Gallone.pdf` | Ancien CV, utilisé comme source |
| `conversation/conversation.md` | Conversation avec Claude, version lisible |
| `conversation/export/` | Export brut de la session Claude Code (transcription, métadonnées) |

## Régénérer le PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=CV_Michel_Gallone_2026.pdf "file://$PWD/CV_Michel_Gallone_2026.html"
```
