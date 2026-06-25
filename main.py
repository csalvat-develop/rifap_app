"""
DiveRescue - Application de gestion d'accident de plongée
Plan de secours interactif FFESSM pour Directeur de Plongée
Flet 0.85 / Python 3.12
"""
import flet as ft
import flet_geolocator as fg

from data import EMERGENCY_CONTACTS, CONDUCT_DATA, TRAME_TEXTE
from views.accueil  import build_accueil_view
from views.alerte   import build_alerte_view
from views.trame    import build_trame_view
from views.bilan    import build_bilan_view
from views.conduite import build_conduite_view

COULEUR_FOND   = "#0A1628"
COULEUR_ACCENT = "#00B4D8"
COULEUR_NAVBAR = "#0D1F3C"


def main(page: ft.Page):
    page.title      = "DiveRescue – Plan de Secours DP"
    page.bgcolor    = COULEUR_FOND
    page.padding    = ft.Padding(0, 0, 0, 0)
    page.theme_mode = ft.ThemeMode.DARK
    page.theme      = ft.Theme(color_scheme_seed=COULEUR_ACCENT)

    # Services instanciés dans main() — s'auto-enregistrent via context.page
    geolocator   = fg.Geolocator()
    url_launcher = ft.UrlLauncher()

    state = {
        "current_tab": 0,
        "bilan": {
            "conscience":  None,
            "respiration": None,
            "signes":      [],
            "profondeur":  "",
            "duree":       "",
            "paliers":     None,
            "gaz":         {"type": "air", "o2": 21, "he": 0},
            "notes":       "",
        },
    }

    content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    nav_bar = ft.NavigationBar(
        selected_index=0,
        bgcolor=COULEUR_NAVBAR,
        indicator_color=COULEUR_ACCENT,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Accueil",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PHONE_OUTLINED,
                selected_icon=ft.Icons.PHONE,
                label="Alerte",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.RECORD_VOICE_OVER_OUTLINED,
                selected_icon=ft.Icons.RECORD_VOICE_OVER,
                label="Trame",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.ASSIGNMENT_OUTLINED,
                selected_icon=ft.Icons.ASSIGNMENT,
                label="Bilan",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MEDICAL_SERVICES_OUTLINED,
                selected_icon=ft.Icons.MEDICAL_SERVICES,
                label="Conduite",
            ),
        ],
        on_change=lambda e: navigate_to(e.control.selected_index),
    )

    def navigate_to(tab_index: int, extra=None):
        state["current_tab"] = tab_index
        nav_bar.selected_index = tab_index
        content_area.controls.clear()
        builders = {
            0: lambda: build_accueil_view(page, navigate_to, state),
            1: lambda: build_alerte_view(page, state, EMERGENCY_CONTACTS, url_launcher),
            2: lambda: build_trame_view(page, state, TRAME_TEXTE, geolocator),
            3: lambda: build_bilan_view(page, state, navigate_to),
            4: lambda: build_conduite_view(page, state, CONDUCT_DATA, url_launcher, extra),
        }
        fn = builders.get(tab_index)
        if fn:
            content_area.controls.append(fn())
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=content_area,
                    expand=True,
                    padding=ft.Padding(0, 0, 0, 0),
                ),
                nav_bar,
            ],
            expand=True,
            spacing=0,
        )
    )

    navigate_to(0)


if __name__ == "__main__":
    ft.run(main)
