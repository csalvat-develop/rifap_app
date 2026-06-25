"""
Vue Alerte - Numeros d'urgence avec appel direct
196 CROSS prioritaire mer + bandeau VHF Canal 16 MAYDAY
15 SAMU pour eau interieure
Flet 0.85 - launch_url est async, utiliser UrlLauncher
"""
import flet as ft
from views.components import (
    COULEUR_CARTE, COULEUR_ACCENT, COULEUR_TEXTE, COULEUR_SUBTIL,
    COULEUR_DANGER, COULEUR_URGENCE, COULEUR_OK,
    en_tete_page, border_all,
)

PRIORITE_CONFIG = {
    "critique": (COULEUR_DANGER,  "●"),
    "urgent":   (COULEUR_URGENCE, "●"),
    "info":     ("#1565C0",       "○"),
    "local":    ("#37474F",       "◌"),
}


def build_alerte_view(
    page: ft.Page,
    state: dict,
    contacts: list,
    url_launcher: ft.UrlLauncher,
) -> ft.Column:

    async def appeler(numero: str):
        n = numero.strip().replace(" ", "").replace("(", "").replace(")", "")
        if n:
            await url_launcher.launch_url(f"tel:{n}")

    # ─── Etat du sélecteur milieu (mer / eau intérieure) ─────────────────────
    milieu_ref = {"milieu": "mer"}
    bandeaux_container = ft.Column(spacing=0)

    def build_bandeaux():
        bandeaux_container.controls.clear()
        is_mer = milieu_ref["milieu"] == "mer"
        bandeaux_container.controls.append(build_sos_principal(is_mer))
        if is_mer:
            bandeaux_container.controls.append(build_vhf_mayday())
        page.update()

    def on_mer(e):
        milieu_ref["milieu"] = "mer"
        build_bandeaux()

    def on_interieur(e):
        milieu_ref["milieu"] = "interieur"
        build_bandeaux()

    # ─── Sélecteur milieu ────────────────────────────────────────────────────
    def build_selecteur():
        is_mer = milieu_ref["milieu"] == "mer"
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "🌊  Mer", size=13,
                            weight=ft.FontWeight.BOLD if is_mer else ft.FontWeight.NORMAL,
                            color="#FFFFFF" if is_mer else COULEUR_SUBTIL,
                        ),
                        bgcolor="#0D47A1" if is_mer else "#112240",
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        padding=ft.Padding(16, 8, 16, 8),
                        ink=True, on_click=on_mer,
                        border=border_all(1, "#0D47A1") if not is_mer else None,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "🏔  Eau intérieure", size=13,
                            weight=ft.FontWeight.BOLD if not is_mer else ft.FontWeight.NORMAL,
                            color="#FFFFFF" if not is_mer else COULEUR_SUBTIL,
                        ),
                        bgcolor=COULEUR_DANGER if not is_mer else "#112240",
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        padding=ft.Padding(16, 8, 16, 8),
                        ink=True, on_click=on_interieur,
                        border=border_all(1, COULEUR_DANGER) if is_mer else None,
                        expand=True,
                    ),
                ],
                spacing=8,
            ),
            padding=ft.Padding(16, 8, 16, 8),
        )

    # ─── Bandeau SOS principal (contextuel mer / intérieur) ──────────────────
    def build_sos_principal(is_mer: bool):
        async def call_principal(e):
            await appeler("196" if is_mer else "15")

        async def call_secondaire(e):
            await appeler("18")

        if is_mer:
            bg_principal    = "#0D47A1"
            num_principal   = "196"
            lab_principal   = "CROSS"
            detail_principal = "Réseau disponible : appeler le 196 EN PRIORITÉ"
            emoji           = "🌊"
            titre           = "MER"
        else:
            bg_principal    = COULEUR_DANGER
            num_principal   = "15"
            lab_principal   = "SAMU"
            detail_principal = "Appeler le 15 EN PRIORITÉ"
            num_secondaire  = "18"
            lab_secondaire  = "Pompiers"
            emoji           = "🏔"
            titre           = "EAU INTÉRIEURE"

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(emoji, size=22),
                            ft.Column(
                                controls=[
                                    ft.Text(titre, size=13,
                                            weight=ft.FontWeight.W_900, color="#FFFFFF"),
                                    ft.Text(detail_principal, size=11, color="#FFCDD2"),
                                ],
                                spacing=1, tight=True, expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.CALL, color="#FFFFFF", size=20),
                                        ft.Column(
                                            controls=[
                                                ft.Text(num_principal, size=22,
                                                        weight=ft.FontWeight.W_900,
                                                        color="#FFFFFF"),
                                                ft.Text(lab_principal, size=10,
                                                        color="#FFCDD2"),
                                            ],
                                            spacing=0, tight=True,
                                        ),
                                    ],
                                    spacing=8, tight=True,
                                ),
                                bgcolor="#B71C1C",
                                on_click=call_principal,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding(16, 10, 16, 10),
                                ),
                                expand=True,
                            ),
                        ] + ([
                            ft.ElevatedButton(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.CALL, color="#FFFFFF", size=18),
                                        ft.Column(
                                            controls=[
                                                ft.Text(num_secondaire, size=18,
                                                        weight=ft.FontWeight.W_900,
                                                        color="#FFFFFF"),
                                                ft.Text(lab_secondaire, size=10,
                                                        color="#FFE0B2"),
                                            ],
                                            spacing=0, tight=True,
                                        ),
                                    ],
                                    spacing=6, tight=True,
                                ),
                                bgcolor="#E65100",
                                on_click=call_secondaire,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding(14, 10, 14, 10),
                                ),
                            ),
                        ] if not is_mer else []),
                        spacing=10,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=bg_principal,
            border_radius=ft.BorderRadius(12, 12, 0, 0),
            padding=ft.Padding(16, 14, 16, 14),
        )

    # ─── Bandeau VHF Canal 16 MAYDAY (mer uniquement) ────────────────────────
    def build_vhf_mayday():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.RADIO, color="#FFFFFF", size=22),
                            ft.Column(
                                controls=[
                                    ft.Text("VHF CANAL 16 — Alerte secondaire",
                                            size=13, weight=ft.FontWeight.W_900,
                                            color="#FFFFFF"),
                                    ft.Text("Si pas de réseau téléphonique",
                                            size=11, color="#FFCDD2"),
                                ],
                                spacing=1, tight=True, expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Trame MAYDAY :", size=11,
                                        weight=ft.FontWeight.BOLD, color="#FFE0B2"),
                                ft.Container(height=4),
                                ft.Text(
                                    "MAYDAY MAYDAY MAYDAY\n"
                                    "Ici [nom du navire]\n"
                                    "Position [GPS]\n"
                                    "Accident de plongée — [nb] victime(s) — [état]\n"
                                    "Demandons assistance médicale urgente\n"
                                    "À vous.",
                                    size=13,
                                    color="#FFFFFF",
                                    font_family="monospace",
                                ),
                            ],
                            spacing=0,
                        ),
                        bgcolor="#7B1111",
                        border_radius=ft.BorderRadius(8, 8, 8, 8),
                        padding=ft.Padding(12, 10, 12, 10),
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        "Un accident de plongée = danger grave et imminent "
                        "→ MAYDAY recommandé par les CROSS (FFESSM 06/2026)",
                        size=10, color="#FFCDD2", italic=True,
                    ),
                ],
                spacing=0,
            ),
            bgcolor="#880000",
            border_radius=ft.BorderRadius(0, 0, 12, 12),
            padding=ft.Padding(16, 14, 16, 14),
        )

    # ─── Cartes contacts ─────────────────────────────────────────────────────
    def contact_card(contact: dict) -> ft.Container:
        prio     = contact.get("priorite", "info")
        couleur_prio, marker = PRIORITE_CONFIG.get(prio, ("#607D8B", "○"))
        editable = contact.get("editable", False)
        numero   = contact.get("numero", "")

        if editable:
            champ_numero = ft.TextField(
                value=numero,
                hint_text="Saisir le numéro",
                keyboard_type=ft.KeyboardType.PHONE,
                text_size=15,
                color=COULEUR_TEXTE,
                hint_style=ft.TextStyle(color=COULEUR_SUBTIL),
                border_color=COULEUR_ACCENT,
                focused_border_color=COULEUR_ACCENT,
                bgcolor="#0A1628",
                border_radius=ft.BorderRadius(8, 8, 8, 8),
                height=44,
                content_padding=ft.Padding(10, 0, 10, 0),
                expand=True,
            )
            async def on_call_edit(e):
                await appeler(champ_numero.value)

            action_widget = ft.Row(
                controls=[
                    champ_numero,
                    ft.IconButton(
                        icon=ft.Icons.CALL,
                        icon_color="#FFFFFF",
                        bgcolor=COULEUR_OK,
                        icon_size=20,
                        on_click=on_call_edit,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                spacing=8,
            )
        else:
            async def on_call(e, n=numero):
                await appeler(n)

            action_widget = ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CALL, color="#FFFFFF", size=18),
                        ft.Text(numero, size=16,
                                weight=ft.FontWeight.W_900, color="#FFFFFF"),
                    ],
                    spacing=8, tight=True,
                ),
                bgcolor=couleur_prio,
                on_click=on_call,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding(12, 8, 12, 8),
                ),
                expand=True,
            )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(marker, color=couleur_prio, size=14),
                                width=16,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(contact["nom"], size=14,
                                            weight=ft.FontWeight.BOLD, color=COULEUR_TEXTE),
                                    ft.Text(contact["description"], size=11,
                                            color=COULEUR_SUBTIL),
                                ],
                                spacing=1, tight=True, expand=True,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Container(height=8),
                    action_widget,
                ],
                spacing=0,
            ),
            bgcolor=COULEUR_CARTE,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(14, 12, 14, 12),
            margin=ft.Padding(0, 0, 0, 8),
        )

    def categorie_section(cat: dict) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Text(cat["categorie"], size=11,
                        weight=ft.FontWeight.BOLD, color=COULEUR_SUBTIL),
                ft.Container(height=6),
                *[contact_card(c) for c in cat["contacts"]],
                ft.Container(height=8),
            ],
            spacing=0,
        )

    # Init bandeaux
    bandeaux_container.controls.append(build_sos_principal(True))
    bandeaux_container.controls.append(build_vhf_mayday())

    return ft.Column(
        controls=[
            en_tete_page("🚨 Alerte & Secours", "Appuyez sur le numéro pour composer"),
            build_selecteur(),
            ft.Container(
                content=bandeaux_container,
                padding=ft.Padding(16, 0, 16, 12),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[categorie_section(cat) for cat in contacts],
                    spacing=0,
                ),
                padding=ft.Padding(16, 0, 16, 16),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
