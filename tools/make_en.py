# Fabrique la version anglaise du site (site/en/) à partir des pages françaises (site/fr/),
# et branche le sélecteur de langue et les balises hreflang des deux côtés.
# Relancer après chaque modification d'une page française : python3 tools/make_en.py
import os, re, sys

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
BASE = "https://michelgallone.ch"
DATE = "2026-11-20"
PAGES = {"index.html": "", "parcours.html": "parcours", "contact.html": "contact"}

SELECTEUR_FR_AVANT = '''<div class="langues" aria-label="Langue">
        <span class="actif" aria-current="true">FR</span>
        <span class="bientot" title="Version anglaise bientôt disponible">EN</span>
      </div>'''
SELECTEUR_FR = '''<div class="langues" aria-label="Langue">
        <span class="actif" aria-current="true">FR</span>
        <a href="../en/{page}" lang="en" hreflang="en" title="English version">EN</a>
      </div>'''
SELECTEUR_EN = '''<div class="langues" aria-label="Language">
        <a href="../fr/{page}" lang="fr" hreflang="fr" title="Version française">FR</a>
        <span class="actif" aria-current="true">EN</span>
      </div>'''


def alternates(chemin):
    return (f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/{chemin}">\n'
            f'  <link rel="alternate" hreflang="en" href="{BASE}/en/{chemin}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{BASE}/fr/{chemin}">')


COMMUN = [
    ('<html lang="fr-CH">', '<html lang="en">'),
    ('<meta property="og:locale" content="fr_CH">',
     '<meta property="og:locale" content="en_GB">\n  <meta property="og:locale:alternate" content="fr_CH">'),
    ('"inLanguage": "fr-CH"', '"inLanguage": "en"'),
    ('Michel Gallone, chef de projet audiovisuel et digital, dans son studio',
     'Michel Gallone, audiovisual and digital project manager, in his studio'),
    ('aria-label="Navigation principale"', 'aria-label="Main navigation"'),
    ('>Profil</a>', '>Profile</a>'),
    ('>Parcours en bref</a>', '>Career at a glance</a>'),
    ('>Parcours complet</a>', '>Full career</a>'),
    ("<h2>Ils m'ont fait confiance</h2>", '<h2>They trusted me</h2>'),
    ('Les Productions 360 Sàrl («&nbsp;26 minutes&nbsp;»)', 'Les Productions 360 Sàrl (“26 minutes”)'),
    ('Robert John «&nbsp;Mutt&nbsp;» Lange', 'Robert John “Mutt” Lange'),
    ('<span>Mes coordonnées</span>', '<span>Contact details</span>'),
]

INDEX = [
    ('<title>Michel Gallone · Chef de projet audiovisuel et digital · Vaud</title>',
     '<title>Michel Gallone · Audiovisual and Digital Project Manager · Vaud, Switzerland</title>'),
    ('content="Michel Gallone, chef de projet audiovisuel et digital, responsable visibilité et marketing (Vaud, Suisse romande). Radio-TV, vidéo, communication. Disponible."',
     'content="Michel Gallone, audiovisual and digital project manager, visibility and marketing manager (Vaud, French-speaking Switzerland). Radio and TV, video, communication. Available."'),
    ('content="Michel Gallone · Chef de projet audiovisuel et digital, responsable visibilité et marketing"',
     'content="Michel Gallone · Audiovisual and digital project manager, visibility and marketing manager"'),
    ('content="Chef de projet audiovisuel et digital, responsable visibilité et marketing en Suisse romande. Disponible pour un poste, un mandat ou une mission."',
     'content="Audiovisual and digital project manager, visibility and marketing manager in French-speaking Switzerland. Available for a position, a contract or an assignment."'),
    ('"name": "Michel Gallone · CV en ligne"', '"name": "Michel Gallone · Online CV"'),
    ('"Chef de projet audiovisuel et digital",\n      "Responsable visibilité et marketing"',
     '"Audiovisual and digital project manager",\n      "Visibility and marketing manager"'),
    ('"description": "Chef de projet audiovisuel et digital, directeur technique radio-TV et responsable communication, visibilité et marketing en Suisse romande."',
     '"description": "Audiovisual and digital project manager, radio and TV technical director, and communication, visibility and marketing manager in French-speaking Switzerland."'),
    ('"name": "Suisse"', '"name": "Switzerland"'),
    ('"Gestion de projet",\n      "Production audiovisuelle",\n      "Infrastructure radio et télévision",\n      "Direction technique",\n      "Communication digitale",\n      "Marketing",\n      "Visibilité et réseaux sociaux",\n      "Production vidéo",\n      "Ingénierie du son",\n      "Studio d\'enregistrement"',
     '"Project management",\n      "Audiovisual production",\n      "Radio and television infrastructure",\n      "Technical direction",\n      "Digital communication",\n      "Marketing",\n      "Visibility and social media",\n      "Video production",\n      "Sound engineering",\n      "Recording studio"'),
    ('"name": "Chef de projet audiovisuel et digital",', '"name": "Audiovisual and digital project manager",'),
    ('"name": "Canton de Vaud, Suisse"', '"name": "Canton of Vaud, Switzerland"'),
    ('"name": "Responsable visibilité et marketing",', '"name": "Visibility and marketing manager",'),
    ('"name": "Suisse romande"', '"name": "French-speaking Switzerland"'),
    ('<span class="statut"><i></i>Disponible · poste, mandat ou mission</span>',
     '<span class="statut"><i></i>Available · position, contract or assignment</span>'),
    ('<h1>Je conçois et pilote vos projets, de la stratégie <em>à&nbsp;la&nbsp;réalisation.</em></h1>',
     '<h1>I design and lead your projects, from strategy <em>to&nbsp;delivery.</em></h1>'),
    ('<span>Chef de projet audiovisuel et digital</span><span>Responsable visibilité et marketing</span>',
     '<span>Audiovisual and digital project manager</span><span>Visibility and marketing manager</span>'),
    ('<p class="accroche accroche-titre">Expertises</p>', '<p class="accroche accroche-titre">Expertise</p>'),
    ('<li>Pilotage de projets audiovisuels et digitaux</li>', '<li>Leading audiovisual and digital projects</li>'),
    ('<li>Stratégie de communication et développement de la visibilité</li>', '<li>Communication strategy and growing visibility</li>'),
    ('<li>Conception et coordination de dispositifs multimédias</li>', '<li>Designing and coordinating multimedia set-ups</li>'),
    ('<li>Direction de production et coordination opérationnelle</li>', '<li>Production management and operational coordination</li>'),
    ('<li><span>Expérience</span>30 ans</li>', '<li><span>Experience</span>30 years</li>'),
    ('<li><span>Lieu</span>Vaud, Suisse romande</li>', '<li><span>Location</span>Vaud, Switzerland</li>'),
    ('<li><span>Langues</span>Français, anglais</li>', '<li><span>Languages</span>French, English</li>'),
    ('<li><span>Nationalité</span>Suisse</li>', '<li><span>Nationality</span>Swiss</li>'),
    ('<span class="surtitre">Profil</span>', '<span class="surtitre">Profile</span>'),
    ('<h2>Le lien entre la direction, les équipes et le public.</h2>',
     '<h2>The link between management, teams and the audience.</h2>'),
    ("<p>Je cadre les projets, je fédère des équipes internationales et je livre des résultats fiables, dans les délais. Ma double culture, technique et managériale, me permet de parler aussi bien à une direction qu'à une régie, et de transformer un objectif de communication en contenus concrets.</p>",
     '<p>I frame projects, bring international teams together and deliver reliable results, on time. My dual background, technical and managerial, lets me talk to a board as easily as to a control room, and turn a communication goal into concrete content.</p>'),
    ('<h3>Gestion de projet de A à Z</h3><p>Cahier des charges, budget, prestataires, planning, mise en service : trois infrastructures audiovisuelles livrées, dont une chaîne radio-TV.</p>',
     '<h3>End-to-end project management</h3><p>Specifications, budget, suppliers, schedule, commissioning: three audiovisual infrastructures delivered, including a radio and TV channel.</p>'),
    ("<h3>Communication et contenus digitaux</h3><p>J'accompagne les PME dans leur communication : films, vidéos, contenus pour le web et les réseaux.</p>",
     '<h3>Communication and digital content</h3><p>I support SMEs with their communication: films, videos, content for the web and social media.</p>'),
    ('<h3>Une carrière internationale</h3><p>Londres, Paris, Marrakech, Montreux : des équipes et des artistes du monde entier, en français comme en anglais.</p>',
     '<h3>An international career</h3><p>London, Paris, Marrakech, Montreux: teams and artists from all over the world, in French and in English.</p>'),
    ('alt="Michel Gallone à la console de son studio de production son et image"',
     'alt="Michel Gallone at the mixing console of his sound and image production studio"'),
    ('<span class="surtitre">Parcours en bref</span>', '<span class="surtitre">Career at a glance</span>'),
    ('<h2>Les jalons.</h2>', '<h2>Milestones.</h2>'),
    ('<span>2000 – auj.</span><b>Sowatt Music Sàrl</b>Communication pour les PME, vidéo, label, production musicale, management artistique, studio de production son et image',
     '<span>2000 – today</span><b>Sowatt Music Sàrl</b>Communication for SMEs, video, record label, music production, artist management, sound and image production studio'),
    ('<span>2026 – auj.</span><b>Loreto1 Trading SA</b>Responsable administratif et visibilité pour cette société immobilière',
     '<span>2026 – today</span><b>Loreto1 Trading SA</b>Administration and visibility manager for this real estate company'),
    ("<b>M Le Media</b>Création d'une chaîne radio-TV, de la conception à l'antenne",
     '<b>M Le Media</b>Built a radio and TV channel, from design to broadcast'),
    ("<b>«&nbsp;26 minutes&nbsp;» · Les Productions 360</b>Mixage audio et mastering final de l'émission, dès la version pilote",
     '<b>“26 minutes” · Les Productions 360</b>Audio mixing and final mastering of the show, from the pilot onwards'),
    ("<b>The Hana Road Music Group</b>Conception d'un complexe de production audio et multimédia. Enregistrements : Van Morrison (avec Bob Rock), Larry Graham",
     '<b>The Hana Road Music Group</b>Design of an audio and multimedia production complex. Recordings: Van Morrison (with Bob Rock), Larry Graham'),
    ("Son et vidéo pour l'événementiel et la TV", 'Sound and video for events and TV'),
    ('<b>Mutt Lange · Sully Sound</b>Studio et personal management : Céline Dion, Britney Spears, Shania Twain',
     '<b>Mutt Lange · Sully Sound</b>Studio and personal management: Céline Dion, Britney Spears, Shania Twain'),
    ('<b>Londres · Paris · Marrakech</b>Studios, post-production TV, centre de production',
     '<b>London · Paris · Marrakech</b>Studios, TV post-production, production centre'),
    ('download>CV en PDF', 'download>CV (PDF, in French)'),
]

PARCOURS = [
    ('<title>Parcours de Michel Gallone · Chef de projet audiovisuel</title>',
     '<title>Michel Gallone’s career · Audiovisual Project Manager</title>'),
    ('content="Parcours de Michel Gallone : direction technique radio-TV, création de studios, ingénieur du son à Londres et Paris, communication pour les PME. Crédits."',
     'content="Michel Gallone’s career: radio and TV technical direction, studio design, sound engineer in London and Paris, communication for SMEs. Credits."'),
    ('content="Parcours de Michel Gallone · Chef de projet audiovisuel"',
     'content="Michel Gallone’s career · Audiovisual project manager"'),
    ('content="Des projets audiovisuels de Londres à Montreux, racontés chapitre par chapitre."',
     'content="Audiovisual projects from London to Montreux, told chapter by chapter."'),
    ('"name": "Parcours de Michel Gallone"', '"name": "Michel Gallone’s career"'),
    ('<span class="surtitre">Parcours</span>', '<span class="surtitre">Career</span>'),
    ('<h1>Les jalons d’une carrière.</h1>', '<h1>Milestones of a career.</h1>'),
    ('<p>Chaque période en quelques lignes.</p>', '<p>Each period in a few lines.</p>'),
    ('<span class="periode-date">2000 – auj.</span>', '<span class="periode-date">2000 – today</span>'),
    ('<small>Fondateur et gérant</small>', '<small>Founder and managing director</small>'),
    ('<li>Communication pour les PME, production de films et de vidéos</li>', '<li>Communication for SMEs, film and video production</li>'),
    ('<li>Production musicale et management artistique</li>', '<li>Music production and artist management</li>'),
    ('<li>Studio de production son et image</li>', '<li>Sound and image production studio</li>'),
    ('<li>Installations audiovisuelles</li>', '<li>Audiovisual installations</li>'),
    ('<li>Label : découverte et production de nouveaux artistes</li>', '<li>Record label: discovering and producing new artists</li>'),
    ('<summary>Projets récents</summary>', '<summary>Recent projects</summary>'),
    ("<i>Création des slides et de l'audio d'une exposition</i>", '<i>Slides and audio for an exhibition</i>'),
    ("<i>Captation des concerts du festival et création de l'Aftermovie<br>Création du contenu viral pendant le festival</i>",
     '<i>Filming of the festival concerts and creation of the aftermovie<br>Viral content created during the festival</i>'),
    ("<i>Création des visuels et du contenu pour une plateforme d'enseignement online</i>",
     '<i>Visuals and content for an online teaching platform</i>'),
    ('<i>Doublage et sous-titrage des films et enregistrement de la Fondation</i>',
     '<i>Dubbing and subtitling of the films, and recordings for the Foundation</i>'),
    ('<span class="periode-date">2026 – auj.</span>', '<span class="periode-date">2026 – today</span>'),
    ('<small>Société immobilière</small>', '<small>Real estate company</small>'),
    ('<li>Responsable administratif et visibilité pour cette société immobilière</li>',
     '<li>Administration and visibility manager for this real estate company</li>'),
    ('<small>Chef de projet et directeur technique · Crissier</small>', '<small>Project manager and technical director · Crissier</small>'),
    ("<li>Création de l'infrastructure radio et TV, de la conception à la mise en service</li>",
     '<li>Built the radio and TV infrastructure, from design to commissioning</li>'),
    ('<li>Coordination des équipes techniques, éditoriales et des prestataires</li>',
     '<li>Coordination of technical and editorial teams and suppliers</li>'),
    ('<li>Supervision des matinales en direct (Canal+)</li>', '<li>Supervision of the live morning shows (Canal+)</li>'),
    ('<span class="periode-date">Depuis 2012</span>', '<span class="periode-date">Since 2012</span>'),
    ('<b>Enregistrements classiques</b>', '<b>Classical recordings</b>'),
    ("<small>Producteur, coordinateur et ingénieur d'enregistrement</small>", '<small>Producer, coordinator and recording engineer</small>'),
    ('<li>Albums pour les pianistes Elizabeth Sombart et Philippe Entremont</li>',
     '<li>Albums for pianists Elizabeth Sombart and Philippe Entremont</li>'),
    ('<li>Séances aux Abbey Road Studios avec le Royal Philharmonic Orchestra</li>',
     '<li>Sessions at Abbey Road Studios with the Royal Philharmonic Orchestra</li>'),
    ('<b>Les Productions 360 Sàrl · «&nbsp;26 minutes&nbsp;»</b>', '<b>Les Productions 360 Sàrl · “26 minutes”</b>'),
    ('<small>Mixage audio et mastering final</small>', '<small>Audio mixing and final mastering</small>'),
    ("<li>Mixage audio et mastering final de l'émission de Vincent Veillon, Vincent Kucholl et Vincent Sager</li>",
     '<li>Audio mixing and final mastering of the show by Vincent Veillon, Vincent Kucholl and Vincent Sager</li>'),
    ('<li>Dès la version pilote, puis pendant les deux années suivantes</li>',
     '<li>From the pilot, then for the following two years</li>'),
    ('<small>Concepteur puis directeur technique du studio · Montreux</small>',
     '<small>Studio designer, then technical director · Montreux</small>'),
    ("<li>Conception et construction d'un complexe de production audio et multimédia haut de gamme</li>",
     '<li>Design and construction of a high-end audio and multimedia production complex</li>'),
    ("<li>Liaison fibre optique jusqu'à l'Auditorium Stravinsky (2m2c)</li>",
     '<li>Fibre-optic link to the Auditorium Stravinsky (2m2c)</li>'),
    ('<i>Enregistrement (tracking) avec Bob Rock</i>', '<i>Recording (tracking) with Bob Rock</i>'),
    ('<i>Enregistrement (tracking)</i>', '<i>Recording (tracking)</i>'),
    ('<small>Son et vidéo événementiel · Montreux, Lausanne, Genève</small>',
     '<small>Event sound and video · Montreux, Lausanne, Geneva</small>'),
    ("<li>Conférences, spectacles et événements d'entreprise : 2m2c, SwissTech Convention Center, Beaulieu, Royal Savoy</li>",
     '<li>Conferences, shows and corporate events: 2m2c, SwissTech Convention Center, Beaulieu, Royal Savoy</li>'),
    ('<li>Captations et émissions TV multicaméra</li>', '<li>Multi-camera filming and TV programmes</li>'),
    ("<small>Réalisateur et producteur · aujourd'hui Carac TV</small>", '<small>Director and producer · now Carac TV</small>'),
    ('<li>Production et réalisation de programmes, du tournage à la diffusion</li>',
     '<li>Production and direction of programmes, from shooting to broadcast</li>'),
    ('<small>Responsable du studio et personal manager · La Tour-de-Peilz</small>',
     '<small>Studio manager and personal manager · La Tour-de-Peilz</small>'),
    ("<li>Gestion du studio lors de l'installation de la société en Suisse romande</li>",
     '<li>Ran the studio when the company set up in French-speaking Switzerland</li>'),
    ('<li>Interface avec les équipes de Céline Dion, Britney Spears, Shania Twain, Bryan Adams, The Corrs</li>',
     '<li>Liaison with the teams of Céline Dion, Britney Spears, Shania Twain, Bryan Adams, The Corrs</li>'),
    ('<i>Up! (mixage), Ka-Ching! (remix), Greatest Hits</i>', '<i>Up! (mixing), Ka-Ching! (remix), Greatest Hits</i>'),
    ('<span>2004 · mixage</span>', '<span>2004 · mixing</span>'),
    ("Don't Let Me Be The Last To Know (mixage)</i>", "Don't Let Me Be The Last To Know (mixing)</i>"),
    ('<b>Londres · Paris · Marrakech · Montreux</b>', '<b>London · Paris · Marrakech · Montreux</b>'),
    ('<li>Londres : chef ingénieur du son de Nomis Studios</li>', '<li>London: chief sound engineer at Nomis Studios</li>'),
    ('<li>Paris : post-production pour Walt Disney, M6 et TF1</li>', '<li>Paris: post-production for Walt Disney, M6 and TF1</li>'),
    ("<li>Marrakech : bras droit du concepteur Tom Hidley pour un centre de production, coordination d'équipes internationales</li>",
     '<li>Marrakech: right-hand man to studio designer Tom Hidley for a production centre, coordinating international teams</li>'),
    ('<li>Montreux : automatisation radio, dont Energy (NRJ) Allemagne ; début de la collaboration avec Mutt Lange</li>',
     '<li>Montreux: radio automation, including Energy (NRJ) Germany; start of the collaboration with Mutt Lange</li>'),
    ('<b>Formation</b>', '<b>Education</b>'),
    ('<li>Recording Arts Degree, Full Sail University, Floride (USA)</li>', '<li>Recording Arts Degree, Full Sail University, Florida (USA)</li>'),
    ('<li>Baccalauréat A2, Lycée Valbert</li>', '<li>Baccalauréat A2 (French high-school diploma), Lycée Valbert</li>'),
    ('<span class="periode-date">Engagement</span>', '<span class="periode-date">Community</span>'),
    ('<b>Associations artistiques</b>', '<b>Arts associations</b>'),
    ('<li>Route 108 : co-fondateur et secrétaire du comité</li>', '<li>Route 108: co-founder and committee secretary</li>'),
    ('<li>Association artistique SAP : co-fondateur</li>', '<li>SAP arts association: co-founder</li>'),
    ('>Tous les crédits sur Discogs ↗</a>', '>All credits on Discogs ↗</a>'),
    ('>Interview dans Headliner Magazine ↗</a>', '>Interview in Headliner Magazine ↗</a>'),
]

CONTACT = [
    ('<title>Contacter Michel Gallone · Chef de projet audiovisuel, Vaud</title>',
     '<title>Contact Michel Gallone · Audiovisual Project Manager, Vaud</title>'),
    ('content="Contacter Michel Gallone, chef de projet audiovisuel et digital dans le canton de Vaud : téléphone, e-mail, LinkedIn et carte de contact (vCard) à enregistrer."',
     'content="Contact Michel Gallone, audiovisual and digital project manager in the canton of Vaud: phone, email, LinkedIn and a contact card (vCard) to save."'),
    ('content="Contacter Michel Gallone · Chef de projet audiovisuel, Vaud"',
     'content="Contact Michel Gallone · Audiovisual project manager, Vaud"'),
    ('content="Chef de projet audiovisuel et digital en Suisse romande. Téléphone, e-mail, LinkedIn et carte de contact à enregistrer."',
     'content="Audiovisual and digital project manager in French-speaking Switzerland. Phone, email, LinkedIn and a contact card to save."'),
    ('"name": "Contacter Michel Gallone"', '"name": "Contact Michel Gallone"'),
    ('alt="Portrait de Michel Gallone, chef de projet audiovisuel et digital"',
     'alt="Portrait of Michel Gallone, audiovisual and digital project manager"'),
    ('<span>Chef de projet audiovisuel et digital</span><span>Responsable visibilité et marketing</span>',
     '<span>Audiovisual and digital project manager</span><span>Visibility and marketing manager</span>'),
    ('Enregistrer le contact</a>', 'Save contact</a>'),
    ('Afficher le QR code</button>', 'Show QR code</button>'),
    ('aria-label="Réseaux"', 'aria-label="Social networks"'),
    ('aria-label="LinkedIn de Michel Gallone"', 'aria-label="Michel Gallone on LinkedIn"'),
    ('aria-label="Instagram de Michel Gallone"', 'aria-label="Michel Gallone on Instagram"'),
    ('aria-label="Facebook de Michel Gallone"', 'aria-label="Michel Gallone on Facebook"'),
    ('Rue de Villars 6A · 1307 Lussery-Villars · Suisse', 'Rue de Villars 6A · 1307 Lussery-Villars · Switzerland'),
    ('<p class="qr-role">Chef de projet audiovisuel et digital</p>', '<p class="qr-role">Audiovisual and digital project manager</p>'),
    ('alt="QR code contenant les coordonnées de Michel Gallone"', 'alt="QR code with Michel Gallone’s contact details"'),
    ("<p class=\"qr-legende\">Scannez avec l'appareil photo du téléphone pour ajouter le contact.</p>",
     '<p class="qr-legende">Scan with your phone’s camera to add the contact.</p>'),
    ('data-qr-fermer>Fermer</button>', 'data-qr-fermer>Close</button>'),
]

PROPRES = {"index.html": INDEX, "parcours.html": PARCOURS, "contact.html": CONTACT}


def remplace(t, a, b, fichier):
    if a not in t:
        sys.exit(f"Introuvable dans {fichier} : {a[:70]!r}")
    return t.replace(a, b)


for page, chemin in PAGES.items():
    src = os.path.join(RACINE, "fr", page)
    fr = open(src, encoding="utf-8").read()

    # --- Page française : sélecteur actif et hreflang (une seule fois) ---
    if SELECTEUR_FR_AVANT in fr:
        fr = fr.replace(SELECTEUR_FR_AVANT, SELECTEUR_FR.format(page=page))
    ancien = f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/{chemin}">'
    if ancien in fr and 'hreflang="x-default"' not in fr:
        fr = fr.replace(ancien, alternates(chemin))
    fr = fr.replace('\n  <!-- <link rel="alternate" hreflang="en" href="https://michelgallone.ch/en/"> : à activer avec la version anglaise -->', '')
    open(src, "w", encoding="utf-8").write(fr)

    # --- Page anglaise ---
    en = fr
    for a, b in COMMUN + PROPRES[page]:
        en = remplace(en, a, b, page)
    en = remplace(en, SELECTEUR_FR.format(page=page), SELECTEUR_EN.format(page=page), page)
    en = en.replace(alternates(chemin), "@@ALT@@")
    en = en.replace(f"{BASE}/fr/", f"{BASE}/en/")
    en = en.replace("@@ALT@@", alternates(chemin))
    en = re.sub(r'"dateModified": "[0-9-]+"', f'"dateModified": "{DATE}"', en)
    os.makedirs(os.path.join(RACINE, "en"), exist_ok=True)
    open(os.path.join(RACINE, "en", page), "w", encoding="utf-8").write(en)
    print("ok", page)
