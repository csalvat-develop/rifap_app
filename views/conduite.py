"""
Vue Conduite à Tenir — Flet 0.85 compatible
Alerte : 196 si mer, 15 si eau intérieure
launch_url est async → utiliser UrlLauncher
"""
import flet as ft
from views.components import (
    COULEUR_CARTE, COULEUR_ACCENT, COULEUR_TEXTE, COULEUR_SUBTIL,
    COULEUR_DANGER, COULEUR_URGENCE, COULEUR_OK, COULEUR_LIGNE,
    en_tete_page, separateur, badge_urgence, numero_etape, border_all,
)
from data import SYMPTOMS_DATA

URGENCE_CONFIG = {
    "critique": COULEUR_DANGER,
    "urgent":   COULEUR_URGENCE,
    "normal":   COULEUR_OK,
}


def build_conduite_view(
    page: ft.Page,
    state: dict,
    conduct_data: dict,
    url_launcher: ft.UrlLauncher,
    symptom_key: str = None,
) -> ft.Column:

    tv = state.get("trame_values", {})
    nature_from_trame = tv.get("nature_id")

    initial_key = symptom_key or nature_from_trame or list(conduct_data.keys())[0]
    selected_key_ref = {"key": initial_key}
    milieu_ref       = {"milieu": "mer"}

    # Le bandeau "depuis la Trame" ne s'affiche que si la selection initiale
    # vient effectivement de la Trame (et pas d'une navigation explicite)
    depuis_trame_ref = {"actif": (symptom_key is None and nature_from_trame is not None)}

    selector_container = ft.Column(spacing=0)
    content_container  = ft.Column(spacing=0)

    async def appeler(numero: str):
        await url_launcher.launch_url(f"tel:{numero}")

    # ─── Sélecteur milieu ────────────────────────────────────────────────────
    def build_milieu_selector():
        is_mer = milieu_ref["milieu"] == "mer"

        def on_mer(e):
            milieu_ref["milieu"] = "mer"
            refresh_all()

        def on_interieur(e):
            milieu_ref["milieu"] = "interieur"
            refresh_all()

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.WATER, color=COULEUR_SUBTIL, size=16),
                    ft.Text("Milieu :", size=12,
                            weight=ft.FontWeight.BOLD, color=COULEUR_SUBTIL),
                    ft.Container(
                        content=ft.Text(
                            "🌊 Mer", size=13,
                            weight=ft.FontWeight.BOLD if is_mer else ft.FontWeight.NORMAL,
                            color="#FFFFFF" if is_mer else COULEUR_SUBTIL,
                        ),
                        bgcolor="#1565C0" if is_mer else "#112240",
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        padding=ft.Padding(14, 6, 14, 6),
                        ink=True, on_click=on_mer,
                        border=border_all(1, "#1565C0") if not is_mer else None,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "🏔 Eau intérieure", size=13,
                            weight=ft.FontWeight.BOLD if not is_mer else ft.FontWeight.NORMAL,
                            color="#FFFFFF" if not is_mer else COULEUR_SUBTIL,
                        ),
                        bgcolor="#2E7D32" if not is_mer else "#112240",
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        padding=ft.Padding(14, 6, 14, 6),
                        ink=True, on_click=on_interieur,
                        border=border_all(1, "#2E7D32") if is_mer else None,
                    ),
                ],
                spacing=8, wrap=True,
            ),
            padding=ft.Padding(16, 8, 16, 4),
        )

    # ─── Chips accident ───────────────────────────────────────────────────────
    def build_symptom_selector():
        chips = []
        for symptom in SYMPTOMS_DATA:
            sid    = symptom["id"]
            is_sel = selected_key_ref["key"] == sid

            def on_chip(e, s=sid):
                selected_key_ref["key"] = s
                depuis_trame_ref["actif"] = False
                refresh_all()

            chips.append(ft.Container(
                content=ft.Text(
                    symptom["titre"], size=12,
                    weight=ft.FontWeight.BOLD if is_sel else ft.FontWeight.NORMAL,
                    color="#FFFFFF" if is_sel else COULEUR_SUBTIL,
                ),
                bgcolor=symptom["couleur"] if is_sel else "#112240",
                border_radius=ft.BorderRadius(20, 20, 20, 20),
                padding=ft.Padding(12, 6, 12, 6),
                ink=True, on_click=on_chip,
                border=border_all(1, symptom["couleur"]) if not is_sel else None,
            ))

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("TYPE D'ACCIDENT", size=11,
                            weight=ft.FontWeight.BOLD, color=COULEUR_SUBTIL),
                    ft.Container(height=6),
                    ft.Row(controls=chips, spacing=6, wrap=True),
                ],
                spacing=0,
            ),
            padding=ft.Padding(16, 6, 16, 8),
        )

    # ─── Carte étape ─────────────────────────────────────────────────────────
    def build_etape_card(etape: dict) -> ft.Container:
        couleur_u = URGENCE_CONFIG.get(etape["urgence"], COULEUR_SUBTIL)
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            numero_etape(etape["num"], couleur_u),
                            ft.Text(etape["titre"], size=14,
                                    weight=ft.FontWeight.BOLD, color=COULEUR_TEXTE,
                                    expand=True),
                            badge_urgence(etape["urgence"]),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Text(etape["detail"], size=13, color=COULEUR_TEXTE),
                        bgcolor="#0A1628",
                        border_radius=ft.BorderRadius(8, 8, 8, 8),
                        padding=ft.Padding(12, 10, 12, 10),
                        border=border_all(1, couleur_u + "40"),
                    ),
                ],
                spacing=0,
            ),
            bgcolor=COULEUR_CARTE,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(14, 12, 14, 12),
            margin=ft.Padding(0, 0, 0, 8),
            border=border_all(1, couleur_u + "30"),
        )

    # ─── À ne pas faire ──────────────────────────────────────────────────────
    def build_ne_pas(ne_pas_list: list) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.WARNING, color=COULEUR_DANGER, size=18),
                            ft.Text("À NE PAS FAIRE", size=12,
                                    weight=ft.FontWeight.BOLD, color=COULEUR_DANGER),
                        ],
                        spacing=6,
                    ),
                    ft.Container(height=8),
                    *[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.BLOCK,
                                                    color=COULEUR_DANGER, size=16),
                                    width=24,
                                ),
                                ft.Text(item, size=13, color="#FFCDD2", expand=True),
                            ],
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        )
                        for item in ne_pas_list
                    ],
                ],
                spacing=6,
            ),
            bgcolor="#1A0A0A",
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(14, 12, 14, 12),
            border=border_all(1, COULEUR_DANGER + "50"),
        )

    # ─── Bandeau O₂ ──────────────────────────────────────────────────────────
    def build_o2_banner(o2_indication: bool, o2_detail: str = None):
        if o2_detail:
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("O2", size=18, weight=ft.FontWeight.W_900, color="#FFFFFF"),
                        ft.Text(o2_detail, size=12, color="#FFFFFF", expand=True),
                    ],
                    spacing=10,
                ),
                bgcolor="#4A148C",
                border_radius=ft.BorderRadius(10, 10, 10, 10),
                padding=ft.Padding(14, 10, 14, 10),
                margin=ft.Padding(0, 0, 0, 8),
            )
        if not o2_indication:
            return ft.Container()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("O2", size=18,
                                    weight=ft.FontWeight.W_900, color="#FFFFFF"),
                            ft.Text("PROTOCOLE OXYGENE NORMALISE FFESSM",
                                    size=11, weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF", expand=True),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            # Cas 1 : victime ventile
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.AIR,
                                                        color="#FFFFFF", size=16),
                                                ft.Text("Ventile", size=12,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#FFFFFF"),
                                            ],
                                            spacing=4,
                                        ),
                                        ft.Text("MHC", size=16,
                                                weight=ft.FontWeight.W_900,
                                                color="#FFFFFF"),
                                        ft.Text("O2 pur — 15 L/min",
                                                size=11, color="#C8E6C9"),
                                    ],
                                    spacing=3, tight=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor="#1B5E20",
                                border_radius=ft.BorderRadius(8, 8, 8, 8),
                                padding=ft.Padding(12, 10, 12, 10),
                                expand=True,
                            ),
                            # Cas 2 : arrêt ventilatoire
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.WARNING,
                                                        color="#FFFFFF", size=16),
                                                ft.Text("Arret vent.", size=12,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#FFFFFF"),
                                            ],
                                            spacing=4,
                                        ),
                                        ft.Text("BAVU", size=16,
                                                weight=ft.FontWeight.W_900,
                                                color="#FFFFFF"),
                                        ft.Text("O2 pur — 15 L/min",
                                                size=11, color="#FFCDD2"),
                                    ],
                                    spacing=3, tight=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor="#B71C1C",
                                border_radius=ft.BorderRadius(8, 8, 8, 8),
                                padding=ft.Padding(12, 10, 12, 10),
                                expand=True,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=0,
            ),
            bgcolor="#0D2818",
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(14, 12, 14, 12),
            margin=ft.Padding(0, 0, 0, 8),
            border=border_all(1, "#2E7D32" + "60"),
        )

    # ─── Bandeau alerte contextuel ───────────────────────────────────────────
    def build_alerte_banner(data: dict):
        if not data.get("alerte_immediate"):
            return ft.Container()

        is_mer = milieu_ref["milieu"] == "mer"
        alerte_mer = data.get("alerte_mer", True)

        if is_mer and alerte_mer:
            num1, lab1 = "196", "CROSS"
            num2, lab2 = "15",  "SAMU"
            conseil    = "Mer : appeler le 196 en premier"
            col2       = "#E65100"
        else:
            num1, lab1 = "15", "SAMU"
            num2, lab2 = "18", "Pompiers"
            conseil    = "Eau intérieure : 15 en premier"
            col2       = "#E65100"

        async def on_num1(e): await appeler(num1)
        async def on_num2(e): await appeler(num2)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SOS, color="#FFFFFF", size=24),
                            ft.Column(
                                controls=[
                                    ft.Text("ALERTE IMMÉDIATE", size=13,
                                            weight=ft.FontWeight.W_900, color="#FFFFFF"),
                                    ft.Text(conseil, size=11, color="#FFCDD2"),
                                ],
                                spacing=1, tight=True, expand=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.CALL, color="#FFFFFF", size=20),
                                        ft.Column(
                                            controls=[
                                                ft.Text(num1, size=22,
                                                        weight=ft.FontWeight.W_900,
                                                        color="#FFFFFF"),
                                                ft.Text(lab1, size=10, color="#FFCDD2"),
                                            ],
                                            spacing=0, tight=True,
                                        ),
                                    ],
                                    spacing=8, tight=True,
                                ),
                                bgcolor="#B71C1C",
                                on_click=on_num1,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding(16, 10, 16, 10),
                                ),
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.CALL, color="#FFFFFF", size=18),
                                        ft.Column(
                                            controls=[
                                                ft.Text(num2, size=18,
                                                        weight=ft.FontWeight.W_900,
                                                        color="#FFFFFF"),
                                                ft.Text(lab2, size=10, color="#FFE0B2"),
                                            ],
                                            spacing=0, tight=True,
                                        ),
                                    ],
                                    spacing=6, tight=True,
                                ),
                                bgcolor=col2,
                                on_click=on_num2,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding(14, 10, 14, 10),
                                ),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=COULEUR_DANGER,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(14, 12, 14, 12),
            margin=ft.Padding(0, 0, 0, 8),
        )

    # ─── Bandeau "depuis la Trame" ──────────────────────────────────────────
    def build_depuis_trame_banner():
        if not depuis_trame_ref["actif"]:
            return ft.Container()
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SYNC, color="#FFFFFF", size=18),
                    ft.Text(
                        "Accident présélectionné depuis la Trame d'appel",
                        size=11, color="#FFFFFF", expand=True,
                    ),
                ],
                spacing=8,
            ),
            bgcolor="#01579B",
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            padding=ft.Padding(12, 8, 12, 8),
            margin=ft.Padding(0, 0, 0, 8),
        )

    # ─── Contenu principal ───────────────────────────────────────────────────
    def build_conduct_content():
        key  = selected_key_ref["key"]
        data = conduct_data.get(key)
        if not data:
            return ft.Text("Données non disponibles.", color=COULEUR_SUBTIL)

        symptom_info = next((s for s in SYMPTOMS_DATA if s["id"] == key), None)
        couleur = symptom_info["couleur"] if symptom_info else COULEUR_ACCENT

        return ft.Column(
            controls=[
                build_depuis_trame_banner(),
                ft.Container(
                    content=ft.Text(data["titre"], size=16,
                                    weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor=couleur,
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(14, 12, 14, 12),
                    margin=ft.Padding(0, 0, 0, 8),
                ),
                build_alerte_banner(data),
                build_o2_banner(data.get("o2_indication", False),
                                data.get("o2_detail")),
                *[build_etape_card(e) for e in data["etapes"]],
                ft.Container(height=4),
                build_ne_pas(data.get("ne_pas", [])),
                ft.Container(height=20),
            ],
            spacing=0,
        )

    def refresh_all():
        selector_container.controls.clear()
        content_container.controls.clear()
        selector_container.controls.append(build_milieu_selector())
        selector_container.controls.append(build_symptom_selector())
        content_container.controls.append(build_conduct_content())
        page.update()

    selector_container.controls.append(build_milieu_selector())
    selector_container.controls.append(build_symptom_selector())
    content_container.controls.append(build_conduct_content())

    return ft.Column(
        controls=[
            en_tete_page("⚕️ Conduite à Tenir", "Étapes par type d'accident"),
            separateur(),
            selector_container,
            separateur(),
            ft.Container(
                content=content_container,
                padding=ft.Padding(16, 8, 16, 8),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
