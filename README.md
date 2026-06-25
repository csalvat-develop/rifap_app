# DiveRescue – Plan de Secours Plongée

Application Android de gestion d'accident de plongée pour Directeur de Plongée (FFESSM).
**Flet 0.85 / Python 3.12**

## Structure

```
dive_rescue/
├── main.py              # Point d'entrée + navigation
├── data.py              # Toutes les données (contacts, trames, conduites)
└── views/
    ├── components.py    # Composants UI réutilisables
    ├── accueil.py       # Écran d'accueil + accès rapide
    ├── alerte.py        # Numéros d'urgence + appel direct
    ├── trame.py         # Script de communication orale
    ├── bilan.py         # Évaluation ABCDE + données plongée
    └── conduite.py      # Conduite à tenir par type d'accident
```

## Installation

```bash
pip install flet==0.85.2
python main.py
```

## Build Android

```bash
flet build apk --project "DiveRescue" --org "fr.plongee.dp"
```

## Fonctionnalités

1. **Accueil** – Accès rapide toutes urgences + liste accidents
2. **Alerte** – Numéros nationaux (15, 18, 112, 196) + COMEX + DAN + contacts locaux éditables
3. **Trame** – Script FFESSM complet avec champs à remplir, prévisualisation
4. **Bilan** – ABCDE : conscience, respiration, circulation, signes neuro, données plongée
5. **Conduite** – 7 types d'accidents : ADD, noyade, barotraumatisme, hyperoxie O₂, essoufflement, hypothermie, panique

## Compatibilité Flet 0.85

Points de vigilance appliqués :
- `ft.run()` au lieu de `ft.app()` (déprécié)
- `ft.NavigationBarDestination` (pas `ft.NavigationDestination`)
- `ft.Colors` (pas `ft.colors` – minuscule)
- `ft.BorderRadius(tl, tr, bl, br)` positionnels
- `ft.Padding(l, t, r, b)` constructeur direct
- `ft.Alignment(x, y)` (pas `ft.alignment.center`)
- `page.show_dialog()` / `page.pop_dialog()` (pas `page.open/close`)
- Navigation par `page.add()` + reconstruction du contenu (pas `page.views`)
