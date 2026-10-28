#!/usr/bin/env python3
"""Crée la carte de visite téléchargeable (vCard) et le QR code de la page Contact.

Usage, depuis la racine du dépôt :
    python3 -m venv tools/.venv && tools/.venv/bin/pip install segno pillow   (une seule fois)
    tools/.venv/bin/python tools/make_contact.py

Écrit dans site/assets/contact/ :
  - Michel_Gallone.vcf   vCard 3.0 avec photo, téléchargée par le bouton « Enregistrer le contact »
  - qr-contact.svg       QR code affiché sur la page (vectoriel, s'adapte à l'écran)
  - qr-contact.png       même QR code en image, pour l'impression ou un message

Le QR code contient une version compacte de la vCard (sans photo ni titre complet) : un téléphone qui le scanne propose
d'ajouter le contact directement, sans connexion et sans dépendre de l'adresse du site.
"""
import base64, io, os, re
import segno
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "contact")

CONTACT = {
    "prenom": "Michel",
    "nom": "Gallone",
    "titre": "Chef de projet audiovisuel et digital · Responsable visibilité et marketing",
    "tel": "+41 79 342 98 80",
    "email": "contact@michelgallone.ch",
    "rue": "Rue de Villars 6A",
    "npa": "1307",
    "ville": "Lussery-Villars",
    "canton": "VD",
    "pays": "Suisse",
    "site": "https://michelgallone.ch",
    "linkedin": "https://www.linkedin.com/in/michelgallone/",
    "instagram": "https://instagram.com/michel.gallone",
    "facebook": "https://facebook.com/michelgallone",
}


def esc(v):  # échappement du texte vCard 3.0
    return v.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def fold(line):  # les lignes vCard sont repliées à 75 octets
    out, cur = [], ""
    for ch in line:
        if len((cur + ch).encode("utf-8")) > 75:
            out.append(cur)
            cur = " " + ch
        else:
            cur += ch
    out.append(cur)
    return "\r\n".join(out)


def vcard(c, photo=None):
    lignes = [
        "BEGIN:VCARD", "VERSION:3.0",
        "N:%s;%s;;;" % (esc(c["nom"]), esc(c["prenom"])),
        "FN:%s %s" % (esc(c["prenom"]), esc(c["nom"])),
        "TITLE:" + esc(c["titre"]),
        "TEL;TYPE=CELL,VOICE:" + re.sub(r"[^\d+]", "", c["tel"]),
        "EMAIL;TYPE=INTERNET:" + c["email"],
        "ADR;TYPE=HOME:;;%s;%s;%s;%s;%s" % (esc(c["rue"]), esc(c["ville"]), c["canton"], c["npa"], esc(c["pays"])),
        "URL:" + c["site"],
        # Apple Contacts lit X-SOCIALPROFILE ; les autres carnets lisent les URL
        "X-SOCIALPROFILE;TYPE=linkedin:" + c["linkedin"],
        "X-SOCIALPROFILE;TYPE=instagram:" + c["instagram"],
        "X-SOCIALPROFILE;TYPE=facebook:" + c["facebook"],
        "item1.URL:" + c["linkedin"], "item1.X-ABLabel:LinkedIn",
        "item2.URL:" + c["instagram"], "item2.X-ABLabel:Instagram",
        "item3.URL:" + c["facebook"], "item3.X-ABLabel:Facebook",
    ]
    if photo:
        lignes.append("PHOTO;ENCODING=b;TYPE=JPEG:" + photo)
    lignes.append("END:VCARD")
    return "\r\n".join(fold(l) for l in lignes) + "\r\n"


def photo_b64():
    im = Image.open(os.path.join(ROOT, "site", "assets", "img", "portrait_carre.jpg")).convert("RGB")
    im.thumbnail((240, 240))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()


def vcard_qr(c):
    """Version compacte pour le QR code : moins de données = code moins dense, plus facile à scanner."""
    lignes = [
        "BEGIN:VCARD", "VERSION:3.0",
        "N:%s;%s" % (c["nom"], c["prenom"]), "FN:%s %s" % (c["prenom"], c["nom"]),
        "TITLE:Chef de projet audiovisuel et digital",
        "TEL;TYPE=CELL:" + re.sub(r"[^\d+]", "", c["tel"]),
        "EMAIL:" + c["email"],
        "ADR:;;%s;%s;;%s;%s" % (c["rue"], c["ville"], c["npa"], c["pays"]),
        "URL:" + c["linkedin"], "URL:" + c["instagram"], "URL:" + c["facebook"],
        "END:VCARD",
    ]
    return "\n".join(lignes)


os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "Michel_Gallone.vcf"), "w", encoding="utf-8", newline="") as f:
    f.write(vcard(CONTACT, photo_b64()))

# QR code : vCard compacte sans photo, niveau de correction M (bon compromis taille / robustesse)
qr = segno.make(vcard_qr(CONTACT), error="m", micro=False)
base = os.path.join(OUT, "qr-contact")
qr.save(base + ".svg", scale=1, border=4, dark="#0A0A0A", light="#FFFFFF", xmldecl=False, svgclass=None, lineclass=None, omitsize=True)
qr.save(base + ".png", scale=12, border=4, dark="#0A0A0A", light="#FFFFFF")
print("vCard et QR code créés dans site/assets/contact/ (QR version %s, correction %s)" % (qr.version, qr.error))
