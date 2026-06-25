"""
Vue Accueil - Ecran principal avec acces rapide
Bandeau regle d'or FFESSM + bandeau O2
Flet 0.85 compatible
"""
import flet as ft
from views.components import (
    COULEUR_ACCENT, COULEUR_TEXTE, COULEUR_SUBTIL,
    COULEUR_DANGER, COULEUR_URGENCE, COULEUR_LIGNE, separateur,
)


def build_accueil_view(page: ft.Page, navigate_to, state: dict) -> ft.Column:

    def btn_urgence(label, icon, tab, couleur):
        def on_click(e):
            navigate_to(tab)
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color="#FFFFFF", size=32),
                    ft.Text(label, size=13, weight=ft.FontWeight.BOLD,
                            color="#FFFFFF", text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6, tight=True,
            ),
            bgcolor=couleur,
            border_radius=ft.BorderRadius(14, 14, 14, 14),
            padding=ft.Padding(12, 16, 12, 16),
            expand=True,
            ink=True,
            on_click=on_click,
            alignment=ft.Alignment(0, 0),
        )

    actions_row1 = ft.Row(
        controls=[
            btn_urgence("ALERTER",       ft.Icons.PHONE,             1, COULEUR_DANGER),
            btn_urgence("TRAME\nAPPEL",  ft.Icons.RECORD_VOICE_OVER, 2, "#D84315"),
        ],
        spacing=10,
    )
    actions_row2 = ft.Row(
        controls=[
            btn_urgence("BILAN\nVICTIME",   ft.Icons.ASSIGNMENT,      3, "#1565C0"),
            btn_urgence("CONDUITE\nA TENIR", ft.Icons.MEDICAL_SERVICES, 4, "#1B5E20"),
        ],
        spacing=10,
    )

    from data import SYMPTOMS_DATA

    def symptome_tile(s):
        def on_click(e):
            navigate_to(4, s["id"])
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.CIRCLE, color=s["couleur"], size=10),
                        width=20,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(s["titre"], size=14, weight=ft.FontWeight.W_600,
                                    color=COULEUR_TEXTE),
                            ft.Text(s["description"], size=11, color=COULEUR_SUBTIL),
                        ],
                        spacing=1, tight=True, expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=COULEUR_SUBTIL, size=18),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(0, 10, 0, 10),
            ink=True,
            on_click=on_click,
        )

    return ft.Column(
        controls=[
            # En-tete
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SCUBA_DIVING, color=COULEUR_ACCENT, size=28),
                        ft.Column(
                            controls=[
                                ft.Text("DiveRescue", size=20,
                                        weight=ft.FontWeight.BOLD, color=COULEUR_TEXTE),
                                ft.Text("Plan de Secours - DP FFESSM",
                                        size=11, color=COULEUR_SUBTIL),
                            ],
                            spacing=1, tight=True,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.Padding(16, 16, 16, 10),
            ),

            # Bandeau regle d'or FFESSM (juin 2026)
            ft.Container(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FORMAT_QUOTE, color="#FFFFFF", size=22),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Quand il y a un doute, il n'y a pas de doute :",
                                        size=12, weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF",
                                    ),
                                    ft.Text(
                                        "on alerte.",
                                        size=14, weight=ft.FontWeight.W_900,
                                        color="#FFFFFF",
                                    ),
                                    ft.Text(
                                        "FFESSM — Recommandation CROSS juin 2026",
                                        size=10, color="#B3E5FC", italic=True,
                                    ),
                                ],
                                spacing=1, tight=True, expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor="#01579B",
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(14, 12, 14, 12),
                ),
                padding=ft.Padding(16, 0, 16, 8),
            ),

            # Bandeau O2
            ft.Container(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.AIR, color="#FFFFFF", size=24),
                            ft.Text(
                                "O2 NORMOBARE — MHC 15 L/min (ventile) · BAVU 15 L/min (ACR)",
                                size=12, weight=ft.FontWeight.BOLD,
                                color="#FFFFFF", expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor=COULEUR_URGENCE,
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(14, 12, 14, 12),
                ),
                padding=ft.Padding(16, 0, 16, 10),
            ),

            # Acces rapide
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("ACCES RAPIDE", size=11,
                                weight=ft.FontWeight.BOLD, color=COULEUR_SUBTIL),
                        ft.Container(height=6),
                        actions_row1,
                        ft.Container(height=8),
                        actions_row2,
                    ],
                    spacing=0,
                ),
                padding=ft.Padding(16, 0, 16, 10),
            ),

            separateur(),

            # Liste accidents
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("ACCIDENTS - CONDUITE A TENIR", size=11,
                                weight=ft.FontWeight.BOLD, color=COULEUR_SUBTIL),
                        ft.Container(height=4),
                        ft.Column(
                            controls=[symptome_tile(s) for s in SYMPTOMS_DATA],
                            spacing=0,
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.Padding(16, 8, 16, 16),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
