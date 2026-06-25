"""
Données métier : contacts, trames, symptômes, conduites à tenir
Référentiel FFESSM / MF
"""

# ─── Contacts d'urgence ─────────────────────────────────────────────────────

EMERGENCY_CONTACTS = [
    {
        "categorie": "URGENCES NATIONALES",
        "contacts": [
            {
                "nom": "SAMU",
                "numero": "15",
                "description": "Service d'aide médicale urgente — eau intérieure en priorité",
                "priorite": "critique",
            },
            {
                "nom": "Pompiers",
                "numero": "18",
                "description": "Secours et sauvetage",
                "priorite": "critique",
            },
            {
                "nom": "CROSS — Sauvetage Maritime",
                "numero": "196",
                "description": "Centre Régional de Surveillance et Sauvetage — mer en priorité",
                "priorite": "critique",
            },
            {
                "nom": "Numéro d'urgence européen",
                "numero": "112",
                "description": "Depuis tout téléphone, y compris sans réseau",
                "priorite": "critique",
            },
        ],
    },
]


# ─── Trame de communication orale ───────────────────────────────────────────

TRAME_TEXTE = {
    "titre": "Trame d'appel aux secours",
    "sous_titre": "Lisez lentement et clairement — répondez aux questions du régulateur",
    "sections": [
        {
            "id": "identification",
            "titre": "1. IDENTIFICATION",
            "couleur": "#00B4D8",
            "items": [
                {
                    "label": "Je suis",
                    "champ": "nom_dp",
                    "placeholder": "[Votre nom et prénom]",
                    "texte": "Je suis __NOM_DP__.",
                },
                {
                    "label": "Nom du site",
                    "champ": "nom_site",
                    "placeholder": "[Nom du spot / site de plongée]",
                    "texte": "Site de plongée : __NOM_SITE__.",
                },
                {
                    "label": "Lieu (rue, commune, département)",
                    "champ": "lieu",
                    "placeholder": "[Auto-rempli via GPS, ou saisie manuelle]",
                    "is_geocoded": True,
                    "texte": "Je me trouve à __LIEU__.",
                },
                {
                    "label": "GPS — Position exacte",
                    "champ": "gps",
                    "is_gps": True,
                    "is_gps_master": True,
                    "texte": "Position exacte du navire (GPS) : __GPS__.",
                },
            ],
        },
        {
            "id": "situation",
            "titre": "2. SITUATION",
            "couleur": "#FF6F00",
            "items": [
                {
                    "label": "Nature de l'accident",
                    "champ": "nature",
                    "options_from_symptoms": True,
                    "texte": "J'ai un accident de plongée : __NATURE__.",
                },
                {
                    "label": "Nombre de victimes",
                    "champ": "nb_victimes",
                    "is_counter": True,
                    "counter_default": 1,
                    "counter_min": 1,
                    "counter_max": 20,
                    "texte": "__NB_VICTIMES__ victime(s) impliquée(s).",
                },
            ],
        },
        {
            "id": "victime",
            "titre": "3. ÉTAT DE LA VICTIME",
            "couleur": "#D32F2F",
            "items": [
                {
                    "label": "Conscience",
                    "champ": "conscience",
                    "options": ["Consciente", "Confuse", "Inconsciente"],
                    "texte": "La victime est __CONSCIENCE__.",
                },
                {
                    "label": "Ventilation",
                    "champ": "ventilation",
                    "options": ["Ventile normalement", "Ventile difficilement", "En arrêt ventilatoire"],
                    "texte": "Ventilation : __VENTILATION__.",
                },
                {
                    "label": "Signes principaux",
                    "champ": "signes",
                    "placeholder": "[Douleurs, paralysie, trouble de la vision, ...]",
                    "texte": "Signes observés : __SIGNES__.",
                },
            ],
        },
        {
            "id": "plongee",
            "titre": "4. DONNÉES DE LA PLONGÉE",
            "couleur": "#1565C0",
            "items": [
                {
                    "label": "Profondeur maximale",
                    "champ": "profondeur",
                    "placeholder": "[X mètres]",
                    "texte": "Profondeur maximale : __PROFONDEUR__ mètres.",
                },
                {
                    "label": "Durée de fond",
                    "champ": "duree",
                    "placeholder": "[X minutes]",
                    "texte": "Durée de fond : __DUREE__ minutes.",
                },
                {
                    "label": "Paliers effectués",
                    "champ": "paliers",
                    "placeholder": "[Oui / Non / Partiellement]",
                    "texte": "Paliers de décompression : __PALIERS__.",
                },
                {
                    "label": "Gaz respiré",
                    "champ": "gaz",
                    "placeholder": "[Air / Nitrox X% / Trimix X%/X%]",
                    "texte": "Gaz utilisé : __GAZ__.",
                },
            ],
        },
        {
            "id": "secours",
            "titre": "5. SECOURS EN COURS",
            "couleur": "#2E7D32",
            "items": [
                {
                    "label": "Oxygène",
                    "champ": "oxygene",
                    "options": ["MHC O2 15 L/min", "BAVU O2 15 L/min", "Non administré"],
                    "texte": "Oxygène normobare administré : __OXYGENE__.",
                },
                {
                    "label": "Position victime",
                    "champ": "position",
                    "options": ["Allongée", "PLS", "Assise"],
                    "texte": "Position de la victime : __POSITION__.",
                },
                {
                    "label": "Couverture",
                    "champ": "couverture",
                    "options": ["Couverte", "Non couverte"],
                    "texte": "Victime couverte : __COUVERTURE__.",
                },
                {
                    "label": "Accès au site",
                    "champ": "acces",
                    "placeholder": "[Route / Hélicoptère / Bateau uniquement]",
                    "texte": "Accès : __ACCES__.",
                },
            ],
        },
        {
            "id": "rappel",
            "titre": "6. RAPPEL",
            "couleur": "#6A1B9A",
            "items": [
                {
                    "label": "Mon numéro de rappel",
                    "champ": "rappel",
                    "placeholder": "[Votre numéro de téléphone]",
                    "texte": "Je reste joignable au __RAPPEL__.",
                },
            ],
        },
        {
            "id": "mayday",
            "titre": "7. MAYDAY VHF — Canal 16 (si pas de réseau)",
            "couleur": "#B71C1C",
            "mayday_only": True,
            "items": [
                {
                    "label": "Nom du navire / support",
                    "champ": "navire",
                    "placeholder": "[Nom du bateau ou support de plongée]",
                    "texte": "MAYDAY MAYDAY MAYDAY — Ici __NAVIRE__.",
                },
                {
                    "label": "Position GPS",
                    "champ": "gps_vhf",
                    "is_gps": True,
                    "texte": "Notre position : __GPS_VHF__.",
                },
                {
                    "label": "Nature et nombre de victimes",
                    "champ": "nature_vhf",
                    "placeholder": "[Ex: accident de plongée, 1 victime inconsciente]",
                    "texte": "Accident de plongée — __NATURE_VHF__.",
                },
                {
                    "label": "Assistance demandée",
                    "champ": "assistance",
                    "placeholder": "[Ex: évacuation médicale urgente]",
                    "texte": "Demandons __ASSISTANCE__ — À vous.",
                },
            ],
        },
    ],
}


# ─── Symptômes ───────────────────────────────────────────────────────────────

SYMPTOMS_DATA = [
    {
        "id": "add",
        "titre": "Accident de Décompression (ADD)",
        "icone": "bubble_chart",
        "couleur": "#D32F2F",
        "description": "Bullage gazeux lors de la remontée",
        "signes": [
            "Douleurs articulaires (bends)",
            "Picotements / engourdissements",
            "Faiblesse musculaire / paralysie",
            "Troubles visuels",
            "Vertiges / nausées",
            "Perte de conscience",
            "Douleur thoracique",
            "Dyspnée",
        ],
    },
    {
        "id": "noyade",
        "titre": "Noyade / Asphyxie",
        "icone": "water",
        "couleur": "#1565C0",
        "description": "Immersion prolongée, inhalation d'eau",
        "signes": [
            "Inconscience",
            "Arrêt ventilatoire / ACR",
            "Cyanose",
            "Toux / crachat mousseux",
            "Hypothermie",
        ],
    },
    {
        "id": "surpression_pulmonaire",
        "titre": "Surpression Pulmonaire (SP)",
        "icone": "warning",
        "couleur": "#C62828",
        "description": "Barotraumatisme pulmonaire — urgence vitale (= ADD type II)",
        "signes": [
            "Douleur thoracique à la remontée",
            "Dyspnée brutale",
            "Emphysème sous-cutané (cou, visage)",
            "Crachat sanglant (hémoptysie)",
            "Troubles neurologiques (embolie gazeuse)",
            "Perte de connaissance",
        ],
    },
    {
        "id": "opi",
        "titre": "Œdème Pulmonaire d'Immersion (OPI)",
        "icone": "water_damage",
        "couleur": "#00838F",
        "description": "Accumulation de liquide dans les poumons liée à l'immersion",
        "signes": [
            "Dyspnée progressive ou brutale",
            "Toux avec expectoration mousseuse, parfois rosée",
            "Sensation d'oppression thoracique",
            "Crépitants à l'auscultation (râles)",
            "Fatigue inhabituelle pendant l'effort",
            "Peut survenir sans notion de remontée rapide",
        ],
    },
    {
        "id": "barotraumatisme",
        "titre": "Barotraumatisme ORL / Dentaire",
        "icone": "hearing",
        "couleur": "#FF6F00",
        "description": "Lésion bénigne causée par variation de pression (oreilles, sinus, dents, masque)",
        "signes": [
            "Douleur auriculaire intense",
            "Perte auditive soudaine",
            "Saignement nasal / auriculaire",
            "Douleur sinusienne",
            "Douleur dentaire",
            "Marques de masque / placage",
        ],
    },
    {
        "id": "hyperoxie",
        "titre": "Hyperoxie / Toxicité O₂",
        "icone": "science",
        "couleur": "#7B1FA2",
        "description": "Excès d'oxygène (Nitrox, profondeur)",
        "signes": [
            "Convulsions",
            "Troubles visuels",
            "Acouphènes",
            "Nausées",
            "Perte de conscience sous l'eau",
        ],
    },
    {
        "id": "essoufflement",
        "titre": "Essoufflement",
        "icone": "air",
        "couleur": "#00695C",
        "description": "Hypercapnie par effort ou détendeur",
        "signes": [
            "Sensation d'étouffement",
            "Respiration rapide et superficielle",
            "Angoisse / panique",
            "Vertiges",
        ],
    },
    {
        "id": "hypothermie",
        "titre": "Hypothermie",
        "icone": "thermostat",
        "couleur": "#0277BD",
        "description": "Abaissement de la température corporelle",
        "signes": [
            "Frissons intenses",
            "Peau froide et pâle",
            "Confusion / somnolence",
            "Pouls faible et lent",
            "Perte de conscience",
        ],
    },
    {
        "id": "syncope",
        "titre": "Syncope (hypoxie / apnée)",
        "icone": "bedtime",
        "couleur": "#5D4037",
        "description": "Perte de connaissance brutale, souvent sous l'eau ou en surface",
        "signes": [
            "Perte de connaissance brutale",
            "Absence de signe avant-coureur (apnée)",
            "Chute / relâchement musculaire",
            "Détendeur perdu / lâché",
            "Récupération possible en quelques minutes",
        ],
    },
    {
        "id": "samba",
        "titre": "Samba (apnée)",
        "icone": "self_improvement",
        "couleur": "#6D4C41",
        "description": "Syncope partielle à la remontée en apnée (hypoxie cérébrale)",
        "signes": [
            "Mouvements saccadés / convulsifs",
            "Regard vide, absence de réponse",
            "Cyanose des lèvres",
            "Perte de contrôle du détendeur/tuba",
            "Survient typiquement en surface après remontée rapide",
        ],
    },
    {
        "id": "panique",
        "titre": "Panique / Détresse",
        "icone": "psychology",
        "couleur": "#827717",
        "description": "Réaction psychologique aiguë",
        "signes": [
            "Agitation extrême",
            "Remontée rapide non contrôlée",
            "Largage intempestif de lestage",
            "Retrait du détendeur",
        ],
    },
]


# ─── Conduites à tenir ───────────────────────────────────────────────────────

CONDUCT_DATA = {
    "add": {
        "titre": "ADD – Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "SORTIR DE L'EAU",
                "detail": "Assister la victime à la sortie. Ne pas la laisser marcher si atteinte neurologique. Allonger horizontalement.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER",
                "detail": "Mer : appeler le 196 (CROSS) EN PREMIER.\nEau intérieure : appeler le 15 (SAMU) EN PREMIER.\nPréciser : ADD suspecté, profondeur, durée, signes neurologiques.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "OXYGÈNE NORMOBARE",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min.\nVictime en arrêt ventilatoire : BAVU avec O₂, débit 15 L/min.\nMaintenir jusqu'à prise en charge médicale. NE JAMAIS REPLONGER.",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "POSITION",
                "detail": "ADD type I (douleurs) : allongé, jambes légèrement surélevées.\nADD type II (neuro) : PLS si inconscient, sinon allongé à plat.\nNE PAS mettre en position assise.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid, du vent et du soleil. Couverture de survie (face dorée vers la victime). Retirer les vêtements mouillés si possible. Isoler du sol froid.",
                "urgence": "urgent",
            },
            {
                "num": 6,
                "titre": "HYDRATATION",
                "detail": "Si conscient et sans trouble de déglutition : eau ou boisson isotonique (500 mL sur 30 min). JAMAIS d'alcool.",
                "urgence": "normal",
            },
            {
                "num": 7,
                "titre": "SURVEILLANCE CONTINUE",
                "detail": "Évaluer toutes les 5 min : conscience, ventilation, signes neurologiques. Noter l'évolution par écrit. Ne pas laisser seul.",
                "urgence": "normal",
            },
            {
                "num": 8,
                "titre": "PRÉPARER LE TRANSFERT",
                "detail": "Rassembler : ordinateur de plongée, profil de plongée, liste des plongées récentes (48h). Accompagner la victime jusqu'au caisson.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS replonger même à faible profondeur",
            "NE PAS administrer de l'aspirine (risque hémorragique)",
            "NE PAS laisser marcher si signes neuro",
            "NE PAS retarder l'évacuation pour « attendre de voir »",
        ],
        "o2_indication": True,
    },
    "noyade": {
        "titre": "Noyade – Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "SÉCURISER ET EXTRAIRE",
                "detail": "Extraire la victime de l'eau. Protéger le rachis cervical si trauma possible. Appeler à l'aide.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER",
                "detail": "Mer : appeler le 196 (CROSS) EN PREMIER.\nEau intérieure : appeler le 15 (SAMU) EN PREMIER.\nPréciser : noyade, état de conscience, ventilation, localisation précise.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "ÉVALUER AB",
                "detail": "A – Airway : libérer les voies aériennes (bascule tête-menton).\nB – Breathing : regarder, écouter, sentir 10 secondes.\nArrêt ventilatoire = ACR → RCP immédiate.",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "RCP SI NÉCESSAIRE",
                "detail": "Arrêt ventilatoire / ACR : RCP immédiate.\n1. Commencer par 5 INSUFFLATIONS INITIALES (insufflations starter).\n2. Puis enchaîner : 30 compressions sternales / 2 insufflations.\nFréquence compressions : 100–120/min, profondeur 5–6 cm.\nDSA dès disponible.",
                "urgence": "critique",
            },
            {
                "num": 5,
                "titre": "OXYGÈNE + POSITION",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min. PLS ou ½-assis selon état.\nVictime en arrêt ventilatoire (ACR) : BAVU avec O₂, débit 15 L/min, en accompagnement de la RCP.\nInconscient ventilant : PLS obligatoire.",
                "urgence": "urgent",
            },
            {
                "num": 6,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Retirer les vêtements mouillés. Couverture de survie (face dorée interne). Protéger du vent et du sol froid. Lutter contre l'hypothermie.",
                "urgence": "urgent",
            },
        ],
        "ne_pas": [
            "NE PAS faire de Heimlich pour expulser l'eau",
            "NE PAS retarder la RCP pour vider les poumons",
            "NE PAS déplacer sans précautions si trauma du rachis suspecté",
            "NE PAS réchauffer trop brutalement (risque fibrillation)",
        ],
        "o2_indication": True,
    },
    "surpression_pulmonaire": {
        "titre": "Surpression Pulmonaire – Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "SORTIR DE L'EAU",
                "detail": "Assister la victime à la sortie. Ne pas la laisser marcher si atteinte neurologique. Allonger horizontalement. NE JAMAIS REPLONGER.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER — URGENCE VITALE",
                "detail": "Traiter comme un ADD type II (embolie gazeuse possible).\nMer : appeler le 196 (CROSS) EN PREMIER.\nEau intérieure : appeler le 15 (SAMU) EN PREMIER.\nPréciser : douleur thoracique à la remontée, dyspnée, emphysème.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "OXYGÈNE NORMOBARE",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min.\nVictime en arrêt ventilatoire : BAVU avec O₂, débit 15 L/min.\nMaintenir jusqu'à prise en charge médicale.",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "POSITION",
                "detail": "Allongé à plat, jambes légèrement surélevées si pas de trouble neurologique.\nPLS si inconscient.\nNE PAS mettre en position assise.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid, du vent et du soleil. Couverture de survie. Isoler du sol froid.",
                "urgence": "urgent",
            },
            {
                "num": 6,
                "titre": "SURVEILLANCE CONTINUE",
                "detail": "Évaluer toutes les 5 min : conscience, ventilation, signes neurologiques. Ne pas laisser seul. Préparer le transfert vers un centre hyperbare.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS replonger même à faible profondeur",
            "NE PAS laisser marcher si signes neuro",
            "NE PAS minimiser une douleur thoracique à la remontée",
            "NE PAS retarder l'évacuation",
        ],
        "o2_indication": True,
    },
    "opi": {
        "titre": "Œdème Pulmonaire d'Immersion – Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "SORTIR DE L'EAU",
                "detail": "Faire cesser l'effort immédiatement. Sortir de l'eau sans délai. Mettre au repos strict, position semi-assise si possible (facilite la ventilation).",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER",
                "detail": "Mer : appeler le 196 (CROSS) EN PREMIER.\nEau intérieure : appeler le 15 (SAMU) EN PREMIER.\nPréciser : dyspnée, toux avec expectoration mousseuse/rosée, sans notion de remontée rapide.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "OXYGÈNE NORMOBARE",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min.\nVictime en arrêt ventilatoire : BAVU avec O₂, débit 15 L/min.",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "POSITION SEMI-ASSISE",
                "detail": "Maintenir en position semi-assise (facilite la respiration), sauf si inconscient (PLS). NE PAS allonger à plat un patient conscient et dyspnéique.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid (facteur favorisant de l'OPI). Couverture de survie. Limiter tout effort supplémentaire.",
                "urgence": "urgent",
            },
            {
                "num": 6,
                "titre": "SURVEILLANCE ET TRANSFERT",
                "detail": "Surveillance continue de la ventilation. Évacuation médicale systématique : risque de récidive et de décompensation rapide.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS allonger à plat un patient dyspnéique conscient",
            "NE PAS sous-estimer : l'OPI peut s'aggraver rapidement",
            "NE PAS faire reprendre l'effort ou la plongée dans la journée",
            "NE PAS confondre avec une noyade simple : pas d'inhalation d'eau",
        ],
        "o2_indication": True,
    },
    "barotraumatisme": {
        "titre": "Barotraumatisme ORL / Dentaire – Conduite à Tenir",
        "alerte_mer": False,
        "alerte_immediate": False,
        "etapes": [
            {
                "num": 1,
                "titre": "ÉVALUATION INITIALE",
                "detail": "Identifier le siège : oreilles, sinus, dents, masque. Évaluer la sévérité. Noter la profondeur et le moment d'apparition.",
                "urgence": "urgent",
            },
            {
                "num": 2,
                "titre": "BARO ORL",
                "detail": "Saignement, douleur, perte auditive : ne pas moucher, ne pas souffler. Position semi-assise. Consultation ORL urgente.",
                "urgence": "urgent",
            },
            {
                "num": 3,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid et du vent si besoin. Maintenir au calme.",
                "urgence": "normal",
            },
            {
                "num": 4,
                "titre": "CONSULTATION MÉDICALE",
                "detail": "Tout barotraumatisme ORL ou dentaire nécessite une consultation médicale. Documenter précisément le profil de plongée.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS replonger avant avis médical",
            "NE PAS se moucher en force",
            "NE PAS confondre avec une surpression pulmonaire (douleur thoracique, dyspnée → voir SP)",
        ],
        "o2_indication": False,
    },
    "hyperoxie": {
        "titre": "Hyperoxie O₂ – Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "REMONTER EN URGENCE",
                "detail": "Convulsions sous l'eau : NE PAS retirer le détendeur. Accompagner la remontée en sécurisant la tête. Surveiller les voies aériennes.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER",
                "detail": "Mer : 196 (CROSS). Eau intérieure : 15 (SAMU).\nPréciser : convulsions, gaz utilisé (Nitrox/%), profondeur lors de l'incident.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "CONVULSIONS EN SURFACE",
                "detail": "Protéger la tête. NE RIEN METTRE dans la bouche. PLS après la crise. Surveiller la ventilation.",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid, du vent et du soleil. Couverture de survie. Maintenir au calme après la crise.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "APRÈS LA CRISE",
                "detail": "Évaluer l'état neurologique. ADD associé possible (remontée rapide). Évacuation médicale.",
                "urgence": "urgent",
            },
        ],
        "ne_pas": [
            "NE PAS retirer le détendeur pendant les convulsions sous l'eau",
            "NE PAS replonger",
            "NE PAS donner O₂ pur en post-crise (risque oxytoxicité)",
            "NE PAS immobiliser les membres en crise",
        ],
        "o2_indication": False,
        "o2_detail": "⚠️ Post-crise : AIR ambiant uniquement — pas d'O₂ pur.",
    },
    "essoufflement": {
        "titre": "Essoufflement – Conduite à Tenir",
        "alerte_mer": False,
        "alerte_immediate": False,
        "etapes": [
            {
                "num": 1,
                "titre": "ARRÊTER L'EFFORT",
                "detail": "Stopper tout effort. S'immobiliser, s'accrocher à un rocher ou à la bouée. Signaler aux équipiers.",
                "urgence": "urgent",
            },
            {
                "num": 2,
                "titre": "VENTILATION CONTRÔLÉE",
                "detail": "Expirer profondément et longuement pour éliminer le CO₂. Inspiration passive. Retour au calme progressif avant toute remontée.",
                "urgence": "urgent",
            },
            {
                "num": 3,
                "titre": "REMONTÉE ASSISTÉE",
                "detail": "Si non résolu en 2 min : remontée assistée accompagnée. Vitesse normale (10–15 m/min). Paliers obligatoires si nécessaire.",
                "urgence": "urgent",
            },
            {
                "num": 4,
                "titre": "COUVRIR LA VICTIME",
                "detail": "En surface : mettre à l'abri du vent. Couverture si frissons. Maintenir allongée et au calme.",
                "urgence": "normal",
            },
            {
                "num": 5,
                "titre": "EN SURFACE",
                "detail": "Repos. Si disponible : masque haute concentration (MHC) — O₂ pur, débit 15 L/min. Bilan : vérifier détendeur, état de fatigue, cause probable.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS hyperventiler (aggrave la situation)",
            "NE PAS remonter en panique (risque ADD ou barotrauma)",
            "NE PAS replonger après un incident sans bilan médical",
        ],
        "o2_indication": True,
    },
    "hypothermie": {
        "titre": "Hypothermie – Conduite à Tenir",
        "alerte_mer": False,
        "alerte_immediate": False,
        "etapes": [
            {
                "num": 1,
                "titre": "SORTIR DU MILIEU FROID",
                "detail": "Mettre à l'abri du vent et du froid. Isoler du sol. Ne pas faire marcher si hypothermie sévère (risque fibrillation).",
                "urgence": "urgent",
            },
            {
                "num": 2,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Retirer les vêtements mouillés (couper si nécessaire). Sécher doucement. Couverture de survie face dorée vers la victime. Couvrir aussi la tête. Isoler du sol froid.",
                "urgence": "urgent",
            },
            {
                "num": 3,
                "titre": "RÉCHAUFFEMENT PASSIF",
                "detail": "Chaleur corporelle ambiante uniquement. Boisson chaude sucrée si conscient sans trouble de déglutition. PAS de bain chaud, PAS de friction.",
                "urgence": "normal",
            },
            {
                "num": 4,
                "titre": "HYPOTHERMIE SÉVÈRE (T° < 30°C)",
                "detail": "Appeler le 15. Prise en charge médicale urgente.\nVictime ventile : MHC — O₂ pur, débit 15 L/min.\nACR : BAVU avec O₂, débit 15 L/min + RCP — « On ne meurt pas hypotherme avant d'être réchauffé ».",
                "urgence": "critique",
            },
        ],
        "ne_pas": [
            "NE PAS frictionner (risque thrombose périphérique)",
            "NE PAS plonger dans un bain très chaud (choc thermique)",
            "NE PAS donner d'alcool",
            "NE PAS arrêter la RCP avant réchauffement médical",
        ],
        "o2_indication": True,
    },
    "syncope": {
        "titre": "Syncope — Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "RAMENER EN SURFACE",
                "detail": "Saisir la victime, maintenir les voies aériennes hors de l'eau (basculer la tête en arrière). Remontée immédiate et assistée. Maintenir le détendeur/tuba en place si possible.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "ALERTER",
                "detail": "Mer : 196 (CROSS) en premier.\nEau intérieure : 15 (SAMU) en premier.\nPréciser : syncope, durée de l'inconscience, contexte (apnée, narcose, etc.).",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "ÉVALUER AB",
                "detail": "A — Airway : libérer les voies aériennes.\nB — Breathing : regarder, écouter, sentir 10 secondes.\nArrêt ventilatoire = ACR → RCP immédiate (5 insufflations puis 30/2).",
                "urgence": "critique",
            },
            {
                "num": 4,
                "titre": "OXYGÈNE",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min.\nVictime en arrêt ventilatoire : BAVU avec O₂, débit 15 L/min.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid et du vent. Couverture de survie. Maintenir allongée et au calme.",
                "urgence": "urgent",
            },
            {
                "num": 6,
                "titre": "SURVEILLANCE",
                "detail": "Même si la victime récupère rapidement, surveillance continue obligatoire. Évacuation médicale systématique (risque de récidive ou d'ADD associé).",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS laisser repartir la victime sans avis médical",
            "NE PAS minimiser une syncope « vite récupérée »",
            "NE PAS replonger dans la journée",
        ],
        "o2_indication": True,
    },
    "samba": {
        "titre": "Samba — Conduite à Tenir",
        "alerte_mer": True,
        "alerte_immediate": True,
        "etapes": [
            {
                "num": 1,
                "titre": "MAINTENIR HORS DE L'EAU",
                "detail": "Maintenir la tête et les voies aériennes hors de l'eau immédiatement. Ne pas immobiliser les membres en mouvement convulsif. Rassurer si conscience partielle.",
                "urgence": "critique",
            },
            {
                "num": 2,
                "titre": "SURVEILLER L'ÉVOLUTION",
                "detail": "Le samba précède souvent la syncope complète : surveiller attentivement l'évolution vers une perte de connaissance totale dans les secondes qui suivent.",
                "urgence": "critique",
            },
            {
                "num": 3,
                "titre": "ALERTER SI AGGRAVATION",
                "detail": "Si évolution vers syncope complète ou arrêt ventilatoire : traiter comme Syncope (alerte 196 mer / 15 intérieur immédiate).",
                "urgence": "urgent",
            },
            {
                "num": 4,
                "titre": "OXYGÈNE PAR PRÉCAUTION",
                "detail": "Victime ventile : masque haute concentration (MHC) — O₂ pur, débit 15 L/min, même après récupération apparente.",
                "urgence": "urgent",
            },
            {
                "num": 5,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Protéger du froid et du vent. Couverture de survie si besoin. Maintenir au repos.",
                "urgence": "normal",
            },
            {
                "num": 6,
                "titre": "BILAN ET REPOS",
                "detail": "Sortir de l'eau. Repos complet. Pas de nouvelle apnée dans la journée. Avis médical recommandé.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS laisser la victime replonger en apnée dans la journée",
            "NE PAS négliger un samba même si la récupération semble totale",
            "NE PAS immobiliser les mouvements convulsifs",
        ],
        "o2_indication": True,
    },
    "panique": {
        "titre": "Panique / Détresse – Conduite à Tenir",
        "alerte_mer": False,
        "alerte_immediate": False,
        "etapes": [
            {
                "num": 1,
                "titre": "APPROCHE SÉCURISÉE",
                "detail": "Approcher par-derrière avec vigilance (risque de coup). Contact visuel rassurant. Signe OK. NE PAS forcer le contact.",
                "urgence": "urgent",
            },
            {
                "num": 2,
                "titre": "CONTRÔLE DE LA REMONTÉE",
                "detail": "Guidage de la remontée à vitesse contrôlée. Conserver le détendeur en bouche. Purgeur de stab accessible. Paliers si profondeur.",
                "urgence": "urgent",
            },
            {
                "num": 3,
                "titre": "EN SURFACE",
                "detail": "Assurer la flottabilité. Gonfler la stab. Rassurer verbalement. Sortir de l'eau rapidement.",
                "urgence": "urgent",
            },
            {
                "num": 4,
                "titre": "COUVRIR LA VICTIME",
                "detail": "Mettre à l'abri du vent et du froid. Couverture de survie si frissons ou état de choc. Maintenir allongée.",
                "urgence": "normal",
            },
            {
                "num": 5,
                "titre": "BILAN POST-INCIDENT",
                "detail": "Évaluer les conséquences d'une remontée rapide (ADD possible). Si doute : MHC — O₂ pur, débit 15 L/min. Soutien psychologique. Déclaration d'incident.",
                "urgence": "normal",
            },
        ],
        "ne_pas": [
            "NE PAS s'approcher de face d'un plongeur en panique",
            "NE PAS forcer la descente",
            "NE PAS négliger un ADD après remontée rapide",
        ],
        "o2_indication": True,
    },
}
