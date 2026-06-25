"""
Vue Bilan – Évaluation de la victime (AB + signes + données plongée)
Flet 0.85 compatible
NOTE MÉDICALE : arrêt ventilatoire = arrêt cardiaque → pas de section C séparée
"""
import flet as ft
from views.components import (
    COULEUR_CARTE, COULEUR_ACCENT, COULEUR_TEXTE, COULEUR_SUBTIL,
    COULEUR_DANGER, COULEUR_URGENCE, COULEUR_OK,
    en_tete_page, separateur, badge_urgence,
)


def _field(hint: str, suffix_label: str = "", bilan: dict = None,
           key: str = "", keyboard=ft.KeyboardType.TEXT,
           multiline: bool = False, min_lines: int = 1,
           max_lines: int = 1) -> ft.TextField:
    kwargs = dict(
        value=bilan.get(key, "") if bilan else "",
        hint_text=hint,
        keyboard_type=keyboard,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=max_lines,
        text_size=15,
        color=COULEUR_TEXTE,
        hint_style=ft.TextStyle(color=COULEUR_SUBTIL),
        border_color=COULEUR_ACCENT,
        focused_border_color=COULEUR_ACCENT,
        bgcolor="#0A1628",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        content_padding=ft.Padding(10, 8, 10, 8),
        expand=True,
    )
    if suffix_label:
        kwargs["suffix"] = ft.Text(suffix_label, color=COULEUR_SUBTIL, size=13)
    if bilan is not None and key:
        kwargs["on_change"] = lambda e, k=key: bilan.update({k: e.control.value})
    return ft.TextField(**kwargs)


def build_bilan_view(page: ft.Page, state: dict, navigate_to) -> ft.Column:
    bilan = state["bilan"]
    tv    = state.get("trame_values", {})

    # ─── Préremplissage depuis la Trame (n'écrase pas une saisie déjà faite) ─
    CONSCIENCE_MAP = {
        "Consciente":   "consciente",
        "Confuse":      "confuse",
        "Inconsciente": "inconsciente",
    }
    VENTILATION_MAP = {
        "Ventile normalement":    "normale",
        "Ventile difficilement":  "difficile",
        "En arrêt ventilatoire":  "absente",
    }

    if not bilan.get("conscience") and tv.get("conscience") in CONSCIENCE_MAP:
        bilan["conscience"] = CONSCIENCE_MAP[tv["conscience"]]

    if not bilan.get("respiration") and tv.get("ventilation") in VENTILATION_MAP:
        bilan["respiration"] = VENTILATION_MAP[tv["ventilation"]]

    if not bilan.get("profondeur") and tv.get("profondeur"):
        bilan["profondeur"] = tv["profondeur"]

    if not bilan.get("duree") and tv.get("duree"):
        bilan["duree"] = tv["duree"]

    # ─── A – Conscience ──────────────────────────────────────────────────────
    conscience_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("A – CONSCIENCE", size=12,
                        weight=ft.FontWeight.BOLD, color=COULEUR_DANGER),
                ft.RadioGroup(
                    value=bilan.get("conscience"),
                    content=ft.Column(
                        controls=[
                            ft.Radio(value="consciente",
                                     label="Consciente – répond aux questions",
                                     label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                            ft.Radio(value="confuse",
                                     label="Confuse / désorientée",
                                     label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                            ft.Radio(value="inconsciente",
                                     label="Inconsciente – ne répond pas",
                                     label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                        ],
                        spacing=4,
                    ),
                    on_change=lambda e: bilan.update({"conscience": e.control.value}),
                ),
            ],
            spacing=8,
        ),
        bgcolor=COULEUR_CARTE,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        padding=ft.Padding(14, 12, 14, 12),
    )

    # ─── B – Ventilation ─────────────────────────────────────────────────────
    # Note : arrêt ventilatoire = considéré comme ACR → RCP immédiate
    ventilation_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("B – VENTILATION", size=12,
                        weight=ft.FontWeight.BOLD, color=COULEUR_DANGER),
                ft.RadioGroup(
                    value=bilan.get("respiration"),
                    content=ft.Column(
                        controls=[
                            ft.Radio(
                                value="normale",
                                label="Normale (12–20 cycles/min)",
                                label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
                            ),
                            ft.Radio(
                                value="rapide",
                                label="Rapide / superficielle",
                                label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
                            ),
                            ft.Radio(
                                value="difficile",
                                label="Difficile / bruyante / dyspnée",
                                label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
                            ),
                            ft.Radio(
                                value="absente",
                                label="Absente → ACR – RCP immédiate",
                                label_style=ft.TextStyle(
                                    color=COULEUR_DANGER, size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                        ],
                        spacing=4,
                    ),
                    on_change=lambda e: bilan.update({"respiration": e.control.value}),
                ),
                # Rappel médical intégré
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINE, color="#90CAF9", size=14),
                            ft.Text(
                                "Arrêt ventilatoire = Arrêt Cardio-Respiratoire"
                                " → RCP + appel 15 sans délai",
                                size=11, color="#90CAF9", expand=True,
                            ),
                        ],
                        spacing=6,
                    ),
                    bgcolor="#0D2137",
                    border_radius=ft.BorderRadius(6, 6, 6, 6),
                    padding=ft.Padding(10, 8, 10, 8),
                ),
            ],
            spacing=8,
        ),
        bgcolor=COULEUR_CARTE,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        padding=ft.Padding(14, 12, 14, 12),
    )

    # ─── C – Signes observés ─────────────────────────────────────────────────
    signes_options = [
        ("douleurs_articulaires", "Douleurs articulaires (bends)"),
        ("paralysie",             "Paralysie / faiblesse membre"),
        ("paresthesies",          "Fourmillements / engourdissements"),
        ("troubles_visuels",      "Troubles visuels"),
        ("vertiges",              "Vertiges / nausées"),
        ("douleur_thoracique",    "Douleur thoracique"),
        ("dyspnee",               "Dyspnée / difficulté respiratoire"),
        ("expectoration_mousseuse", "Expectoration mousseuse/rosée (OPI)"),
        ("convulsions",           "Convulsions"),
        ("cyanose",               "Cyanose (lèvres / ongles bleutés)"),
        ("confusion",             "Confusion / amnésie"),
        ("douleur_oreilles",      "Douleur auriculaire / saignement"),
        ("hypothermie_signe",     "Refroidissement / frissons"),
    ]

    signes_actuels = set(bilan.get("signes", []))

    def on_signe_change(signe_id, e):
        if e.control.value:
            signes_actuels.add(signe_id)
        else:
            signes_actuels.discard(signe_id)
        bilan["signes"] = list(signes_actuels)

    checkboxes = [
        ft.Checkbox(
            label=label,
            value=(sid in signes_actuels),
            active_color=COULEUR_ACCENT,
            label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
            on_change=lambda e, s=sid: on_signe_change(s, e),
        )
        for sid, label in signes_options
    ]

    signes_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("C – SIGNES OBSERVÉS", size=12,
                        weight=ft.FontWeight.BOLD, color=COULEUR_URGENCE),
                ft.Text("Cocher tous les signes présents",
                        size=11, color=COULEUR_SUBTIL),
                ft.Container(height=4),
                ft.Column(controls=checkboxes, spacing=2),
            ],
            spacing=4,
        ),
        bgcolor=COULEUR_CARTE,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        padding=ft.Padding(14, 12, 14, 12),
    )

    # ─── D – Données plongée ─────────────────────────────────────────────────
    field_prof  = _field("Ex: 40", "m",   bilan, "profondeur", ft.KeyboardType.NUMBER)
    field_duree = _field("Ex: 35", "min", bilan, "duree",      ft.KeyboardType.NUMBER)
    field_notes = _field(
        "Observations, antécédents, médicaments...",
        bilan=bilan, key="notes",
        multiline=True, min_lines=3, max_lines=5,
    )
    field_notes.text_size = 13

    paliers_group = ft.RadioGroup(
        value=bilan.get("paliers"),
        content=ft.Row(
            controls=[
                ft.Radio(value="oui",     label="Oui",
                         label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                ft.Radio(value="non",     label="Non",
                         label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                ft.Radio(value="partiel", label="Partiel",
                         label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
                ft.Radio(value="inconnu", label="Inconnu",
                         label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14)),
            ],
            spacing=8, wrap=True,
        ),
        on_change=lambda e: bilan.update({"paliers": e.control.value}),
    )

    plongee_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("D – DONNÉES PLONGÉE", size=12,
                        weight=ft.FontWeight.BOLD, color="#42A5F5"),
                ft.Container(height=4),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Profondeur max.", size=11, color=COULEUR_SUBTIL),
                                field_prof,
                            ],
                            spacing=4, expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Durée de fond", size=11, color=COULEUR_SUBTIL),
                                field_duree,
                            ],
                            spacing=4, expand=True,
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(height=8),
                ft.Text("Paliers effectués", size=11, color=COULEUR_SUBTIL),
                paliers_group,
                ft.Container(height=8),
                ft.Text("Notes / Observations", size=11, color=COULEUR_SUBTIL),
                field_notes,
            ],
            spacing=4,
        ),
        bgcolor=COULEUR_CARTE,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        padding=ft.Padding(14, 12, 14, 12),
    )

    # ─── Actions bas ─────────────────────────────────────────────────────────
    def reset_bilan(e):
        def on_confirm(ev):
            state["bilan"] = {
                "conscience": None, "respiration": None,
                "signes": [], "profondeur": "", "duree": "",
                "paliers": None, "gaz": {"type": "air", "o2": 21, "he": 0},
                "notes": "",
            }
            page.pop_dialog()
            navigate_to(3)

        def on_cancel(ev):
            page.pop_dialog()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("Réinitialiser le bilan ?", color=COULEUR_TEXTE,
                          weight=ft.FontWeight.BOLD),
            content=ft.Text("Toutes les données seront effacées.",
                            color=COULEUR_SUBTIL, size=14),
            actions=[
                ft.TextButton(
                    content=ft.Text("Annuler", color=COULEUR_SUBTIL),
                    on_click=on_cancel,
                ),
                ft.TextButton(
                    content=ft.Text("Réinitialiser", color=COULEUR_DANGER),
                    on_click=on_confirm,
                ),
            ],
            bgcolor="#112240",
            shape=ft.RoundedRectangleBorder(radius=12),
        ))

    prefill_actif = bool(
        tv.get("conscience") in CONSCIENCE_MAP or
        tv.get("ventilation") in VENTILATION_MAP
    )

    return ft.Column(
        controls=[
            en_tete_page("📋 Bilan Victime", "AB – Évaluation systématique"),

            # Bandeau info préremplissage depuis Trame
            ft.Container(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SYNC, color="#FFFFFF", size=18),
                            ft.Text(
                                "Conscience / ventilation préremplies depuis la Trame",
                                size=11, color="#FFFFFF", expand=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor="#01579B",
                    border_radius=ft.BorderRadius(8, 8, 8, 8),
                    padding=ft.Padding(12, 8, 12, 8),
                ),
                padding=ft.Padding(16, 0, 16, 8),
            ) if prefill_actif else ft.Container(),

            # Bandeau ACR
            ft.Container(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FAVORITE, color="#FFFFFF", size=20),
                            ft.Text(
                                "Arrêt ventilatoire = ACR → RCP + 15",
                                size=13, weight=ft.FontWeight.BOLD,
                                color="#FFFFFF", expand=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=COULEUR_DANGER,
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(14, 10, 14, 10),
                ),
                padding=ft.Padding(16, 0, 16, 10),
            ),

            ft.Container(
                content=ft.Column(
                    controls=[
                        conscience_section,
                        ft.Container(height=8),
                        ventilation_section,
                        ft.Container(height=8),
                        signes_section,
                        ft.Container(height=8),
                        plongee_section,
                    ],
                    spacing=0,
                ),
                padding=ft.Padding(16, 0, 16, 8),
            ),

            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.REFRESH, color=COULEUR_SUBTIL, size=18),
                                    ft.Text("Reset", color=COULEUR_SUBTIL, size=13),
                                ],
                                spacing=6, tight=True,
                            ),
                            on_click=reset_bilan,
                            style=ft.ButtonStyle(
                                side=ft.border.BorderSide(1, COULEUR_SUBTIL),
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.MEDICAL_SERVICES,
                                            color="#FFFFFF", size=18),
                                    ft.Text("Conduite à tenir",
                                            color="#FFFFFF", size=13,
                                            weight=ft.FontWeight.BOLD),
                                ],
                                spacing=8, tight=True,
                            ),
                            bgcolor=COULEUR_ACCENT,
                            on_click=lambda e: navigate_to(4),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding(16, 12, 16, 12),
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.Padding(16, 0, 16, 20),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
