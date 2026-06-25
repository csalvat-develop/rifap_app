"""
Vue Trame - Script de communication orale avec champs a remplir
- options          -> boutons radio statiques
- options_from_symptoms -> boutons radio generes depuis SYMPTOMS_DATA
- is_counter        -> compteur +/- avec valeur par defaut
- is_gps            -> bouton de localisation (synchronises entre eux)
- is_geocoded       -> champ rempli automatiquement par geocodage inverse
                       (API Geoplateforme IGN) a partir du GPS obtenu
Section 7 MAYDAY VHF canal 16 (mer uniquement, en rouge)
Flet 0.85 compatible

Les valeurs choisies (nature accident, conscience, ventilation, oxygene,
position, couverture) sont ecrites dans state["trame_values"] pour etre
reutilisees par les ecrans Bilan et Conduite a tenir.
"""
import flet as ft
import flet_geolocator as fg
import httpx
from views.components import (
    COULEUR_ACCENT, COULEUR_TEXTE, COULEUR_SUBTIL,
    COULEUR_OK, COULEUR_DANGER, en_tete_page,
)
from data import SYMPTOMS_DATA

# API de geocodage inverse de la Geoplateforme IGN (remplace l'ancienne API
# BAN api-adresse.data.gouv.fr, decommissionnee fin janvier 2026)
GEOCODE_REVERSE_URL = "https://data.geopf.fr/geocodage/reverse"


async def reverse_geocode(lat: float, lon: float) -> str | None:
    """Retourne 'rue commune (departement)' ou 'commune (departement)' ou None."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                GEOCODE_REVERSE_URL,
                params={"lon": lon, "lat": lat, "index": "address", "limit": 1},
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            features = data.get("features", [])
            if not features:
                return None

            props = features[0].get("properties", {})

            def _first(val):
                if isinstance(val, list):
                    return val[0] if val else None
                return val

            rue      = _first(props.get("street")) or _first(props.get("name"))
            commune  = _first(props.get("city"))
            postcode = _first(props.get("postcode"))
            citycode = _first(props.get("citycode"))
            departement = None
            if citycode and len(str(citycode)) >= 2:
                departement = str(citycode)[:2]
            elif postcode and len(str(postcode)) >= 2:
                departement = str(postcode)[:2]

            parts = []
            if rue:
                parts.append(str(rue))
            if commune:
                if departement:
                    parts.append(f"{commune} ({departement})")
                else:
                    parts.append(str(commune))
            elif departement:
                parts.append(f"département {departement}")

            return ", ".join(parts) if parts else None
    except Exception:
        return None


def build_trame_view(
    page: ft.Page,
    state: dict,
    trame: dict,
    geolocator: fg.Geolocator,
) -> ft.Column:

    # Stockage partage pour Bilan / Conduite a tenir
    if "trame_values" not in state:
        state["trame_values"] = {}
    tv = state["trame_values"]

    fields: dict[str, ft.TextField] = {}
    radios: dict[str, dict]         = {}
    counters: dict[str, dict]       = {}
    gps_fields: dict[str, ft.TextField] = {}
    gps_status_texts: list[ft.Text]     = []
    geocoded_refs: dict = {"field": None, "status": None}

    # ─── GPS partage entre sections ──────────────────────────────────────────
    async def do_locate(e):
        for st in gps_status_texts:
            st.value = "Localisation en cours..."
            st.color = COULEUR_SUBTIL
        page.update()
        try:
            perm = await geolocator.request_permission()
            if perm in (
                fg.GeolocatorPermissionStatus.DENIED,
                fg.GeolocatorPermissionStatus.DENIED_FOREVER,
            ):
                for st in gps_status_texts:
                    st.value = "Permission GPS refusee"
                    st.color = COULEUR_DANGER
                page.update()
                return

            pos = await geolocator.get_current_position(
                configuration=fg.GeolocatorConfiguration(
                    accuracy=fg.GeolocatorPositionAccuracy.HIGH,
                )
            )
            lat_f = pos.latitude
            lon_f = pos.longitude
            lat = f"{lat_f:.5f}" if lat_f is not None else "?"
            lon = f"{lon_f:.5f}" if lon_f is not None else "?"
            acc = int(pos.accuracy or 0)
            valeur = f"{lat}, {lon}"

            for f in gps_fields.values():
                f.value = valeur
            for st in gps_status_texts:
                st.value = f"Position obtenue (+/-{acc} m)"
                st.color = COULEUR_OK
            tv["gps"] = valeur
            page.update()

            # Géocodage inverse automatique pour remplir le champ "Lieu"
            if lat_f is not None and lon_f is not None and geocoded_refs["field"]:
                geocoded_refs["status"].value = "Recherche de l'adresse..."
                geocoded_refs["status"].color = COULEUR_SUBTIL
                page.update()

                adresse = await reverse_geocode(lat_f, lon_f)
                if adresse:
                    geocoded_refs["field"].value = adresse
                    geocoded_refs["status"].value = "Adresse trouvée automatiquement"
                    geocoded_refs["status"].color = COULEUR_OK
                    tv["lieu"] = adresse
                else:
                    geocoded_refs["status"].value = (
                        "Adresse introuvable — saisie manuelle possible"
                    )
                    geocoded_refs["status"].color = COULEUR_SUBTIL
                page.update()

        except Exception as ex:
            for st in gps_status_texts:
                st.value = f"Erreur GPS : {ex}"
                st.color = COULEUR_DANGER
            page.update()

    def build_geocoded_widget(item: dict, section_id: str, couleur: str,
                               label_color: str, preview_color: str,
                               tv_key: str) -> ft.Column:
        fkey = f"{section_id}_{item['champ']}"
        champ_key = item["champ"].upper()

        preview_text = ft.Text(
            item["texte"].replace(f"__{champ_key}__", "[ ... ]"),
            size=12, color=preview_color, italic=True,
        )
        geocode_status = ft.Text("", size=11, color=COULEUR_SUBTIL)

        def on_field_change(e):
            val = e.control.value
            preview_text.value = item["texte"].replace(
                f"__{champ_key}__", val if val else "[ ... ]"
            )
            tv[tv_key] = val
            page.update()

        lieu_field = ft.TextField(
            hint_text=item.get("placeholder", ""),
            value="",
            text_size=14,
            color=COULEUR_TEXTE,
            hint_style=ft.TextStyle(color=COULEUR_SUBTIL),
            border_color=couleur,
            focused_border_color=couleur,
            bgcolor="#0A1628",
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            content_padding=ft.Padding(10, 8, 10, 8),
            expand=True,
            on_change=on_field_change,
        )
        fields[fkey] = lieu_field
        geocoded_refs["field"]  = lieu_field
        geocoded_refs["status"] = geocode_status

        async def on_refresh(e):
            gps_val = tv.get("gps")
            if not gps_val or "," not in gps_val:
                geocode_status.value = "Obtenez d'abord le GPS ci-dessous"
                geocode_status.color = COULEUR_DANGER
                page.update()
                return
            try:
                lat_s, lon_s = gps_val.split(",")
                lat_f, lon_f = float(lat_s.strip()), float(lon_s.strip())
            except ValueError:
                return
            geocode_status.value = "Recherche de l'adresse..."
            geocode_status.color = COULEUR_SUBTIL
            page.update()
            adresse = await reverse_geocode(lat_f, lon_f)
            if adresse:
                lieu_field.value = adresse
                geocode_status.value = "Adresse trouvée automatiquement"
                geocode_status.color = COULEUR_OK
                tv[tv_key] = adresse
                preview_text.value = item["texte"].replace(f"__{champ_key}__", adresse)
            else:
                geocode_status.value = "Adresse introuvable — saisie manuelle"
                geocode_status.color = COULEUR_SUBTIL
            page.update()

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                ft.Row(
                    controls=[
                        lieu_field,
                        ft.IconButton(
                            icon=ft.Icons.LOCATION_SEARCHING,
                            icon_color="#FFFFFF",
                            bgcolor=couleur,
                            icon_size=20,
                            tooltip="Retrouver l'adresse depuis le GPS",
                            on_click=on_refresh,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    spacing=8,
                ),
                geocode_status,
                preview_text,
                ft.Container(height=4),
            ],
            spacing=4,
        )

    def build_gps_widget(item: dict, label_color: str, preview_color: str,
                          is_mayday: bool) -> ft.Column:
        fkey = item["champ"]
        gps_field = ft.TextField(
            hint_text="Appuyez sur l'icone pour localiser",
            value="",
            text_size=14,
            color="#FFFFFF" if is_mayday else COULEUR_TEXTE,
            hint_style=ft.TextStyle(color="#FFCDD2" if is_mayday else COULEUR_SUBTIL),
            border_color="#FF5252" if is_mayday else COULEUR_ACCENT,
            focused_border_color="#FF5252" if is_mayday else COULEUR_ACCENT,
            bgcolor="#5B0000" if is_mayday else "#0A1628",
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            content_padding=ft.Padding(10, 8, 10, 8),
            expand=True,
            read_only=True,
        )
        gps_status = ft.Text("", size=11, color=COULEUR_SUBTIL)
        gps_fields[fkey] = gps_field
        gps_status_texts.append(gps_status)

        champ_key = item["champ"].upper()
        preview = item["texte"].replace(f"__{champ_key}__", "[ ... ]")

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                ft.Row(
                    controls=[
                        gps_field,
                        ft.IconButton(
                            icon=ft.Icons.MY_LOCATION,
                            icon_color="#FFFFFF",
                            bgcolor="#B71C1C" if is_mayday else COULEUR_ACCENT,
                            icon_size=22,
                            tooltip="Obtenir ma position GPS",
                            on_click=do_locate,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    spacing=8,
                ),
                gps_status,
                ft.Text(preview, size=12, color=preview_color, italic=True),
                ft.Container(height=4),
            ],
            spacing=4,
        )

    def build_radio_widget(item: dict, section_id: str, couleur: str,
                            label_color: str, preview_color: str,
                            options: list, tv_key: str = None) -> ft.Column:
        fkey = f"{section_id}_{item['champ']}"
        champ_key = item["champ"].upper()
        preview_text = ft.Text(
            item["texte"].replace(f"__{champ_key}__", "[ ... ]"),
            size=12, color=preview_color, italic=True,
        )

        def on_change(e):
            radios[fkey]["value"] = e.control.value
            preview_text.value = item["texte"].replace(
                f"__{champ_key}__", e.control.value or "[ ... ]"
            )
            if tv_key:
                tv[tv_key] = e.control.value
            page.update()

        radio_group = ft.RadioGroup(
            value=None,
            content=ft.Column(
                controls=[
                    ft.Radio(
                        value=opt, label=opt,
                        label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
                    )
                    for opt in options
                ],
                spacing=2,
            ),
            on_change=on_change,
        )
        radios[fkey] = {"value": None, "group": radio_group}

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                radio_group,
                preview_text,
                ft.Container(height=4),
            ],
            spacing=4,
        )

    def build_symptom_radio_widget(item: dict, section_id: str, couleur: str,
                                    label_color: str, preview_color: str) -> ft.Column:
        """Boutons radio generes depuis SYMPTOMS_DATA - meme liste que Conduite a tenir."""
        fkey = f"{section_id}_{item['champ']}"
        champ_key = item["champ"].upper()
        preview_text = ft.Text(
            item["texte"].replace(f"__{champ_key}__", "[ ... ]"),
            size=12, color=preview_color, italic=True,
        )

        def on_change(e):
            symptom_id = e.control.value
            symptom = next((s for s in SYMPTOMS_DATA if s["id"] == symptom_id), None)
            label = symptom["titre"] if symptom else symptom_id
            radios[fkey]["value"] = label
            preview_text.value = item["texte"].replace(f"__{champ_key}__", label or "[ ... ]")
            tv["nature_id"]    = symptom_id
            tv["nature_label"] = label
            page.update()

        radio_group = ft.RadioGroup(
            value=None,
            content=ft.Column(
                controls=[
                    ft.Radio(
                        value=s["id"], label=s["titre"],
                        label_style=ft.TextStyle(color=COULEUR_TEXTE, size=14),
                    )
                    for s in SYMPTOMS_DATA
                ],
                spacing=2,
            ),
            on_change=on_change,
        )
        radios[fkey] = {"value": None, "group": radio_group}

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                radio_group,
                preview_text,
                ft.Container(height=4),
            ],
            spacing=4,
        )

    def build_counter_widget(item: dict, section_id: str, couleur: str,
                              label_color: str, preview_color: str) -> ft.Column:
        fkey = f"{section_id}_{item['champ']}"
        champ_key = item["champ"].upper()
        default_val = item.get("counter_default", 1)
        cmin = item.get("counter_min", 1)
        cmax = item.get("counter_max", 99)

        counters[fkey] = {"value": default_val}

        value_text = ft.Text(str(default_val), size=20,
                              weight=ft.FontWeight.W_900, color=COULEUR_TEXTE)
        preview_text = ft.Text(
            item["texte"].replace(f"__{champ_key}__", str(default_val)),
            size=12, color=preview_color, italic=True,
        )

        def update_preview():
            preview_text.value = item["texte"].replace(
                f"__{champ_key}__", str(counters[fkey]["value"])
            )

        def on_minus(e):
            v = counters[fkey]["value"]
            if v > cmin:
                v -= 1
                counters[fkey]["value"] = v
                value_text.value = str(v)
                update_preview()
                tv["nb_victimes"] = v
                page.update()

        def on_plus(e):
            v = counters[fkey]["value"]
            if v < cmax:
                v += 1
                counters[fkey]["value"] = v
                value_text.value = str(v)
                update_preview()
                tv["nb_victimes"] = v
                page.update()

        tv["nb_victimes"] = default_val

        counter_row = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                    icon_color=couleur,
                    icon_size=28,
                    on_click=on_minus,
                ),
                ft.Container(
                    content=value_text,
                    width=50,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                    icon_color=couleur,
                    icon_size=28,
                    on_click=on_plus,
                ),
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.START,
        )

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                counter_row,
                preview_text,
                ft.Container(height=4),
            ],
            spacing=4,
        )

    def build_text_widget(item: dict, section_id: str, couleur: str,
                           is_mayday: bool, tv_key: str = None) -> ft.Column:
        fkey = f"{section_id}_{item['champ']}"
        txt_color    = "#FFFFFF" if is_mayday else COULEUR_TEXTE
        hint_color   = "#FFCDD2" if is_mayday else COULEUR_SUBTIL
        border_color = "#FF5252" if is_mayday else couleur
        bg_color     = "#5B0000" if is_mayday else "#0A1628"

        champ_key     = item["champ"].upper()
        label_color   = "#FFCDD2" if is_mayday else couleur
        preview_color = "#FFAB91" if is_mayday else "#78909C"
        preview_text  = ft.Text(
            item["texte"].replace(f"__{champ_key}__", "[ ... ]"),
            size=12, color=preview_color, italic=True,
        )

        def on_change(e):
            val = e.control.value
            preview_text.value = item["texte"].replace(
                f"__{champ_key}__", val if val else "[ ... ]"
            )
            if tv_key:
                tv[tv_key] = val
            page.update()

        if fkey not in fields:
            fields[fkey] = ft.TextField(
                hint_text=item.get("placeholder", ""),
                value="",
                text_size=14,
                color=txt_color,
                hint_style=ft.TextStyle(color=hint_color),
                border_color=border_color,
                focused_border_color=border_color,
                bgcolor=bg_color,
                border_radius=ft.BorderRadius(8, 8, 8, 8),
                content_padding=ft.Padding(10, 8, 10, 8),
                expand=True,
                on_change=on_change,
            )

        return ft.Column(
            controls=[
                ft.Text(item["label"], size=11,
                        weight=ft.FontWeight.BOLD, color=label_color),
                fields[fkey],
                preview_text,
                ft.Container(height=4),
            ],
            spacing=4,
        )

    # Champs dont la valeur doit etre propagee vers Bilan/Conduite
    TV_KEYS = {
        "conscience": "conscience",
        "ventilation": "ventilation",
        "oxygene": "oxygene",
        "position": "position",
        "couverture": "couverture",
        "nom_site": "nom_site",
        "lieu": "lieu",
    }

    # ─── Construction d'une section ──────────────────────────────────────────
    def build_section(section: dict) -> ft.Container:
        couleur   = section["couleur"]
        is_mayday = section.get("mayday_only", False)
        items_controls = []

        for item in section["items"]:
            champ = item["champ"]
            label_color   = "#FFCDD2" if is_mayday else couleur
            preview_color = "#FFAB91" if is_mayday else "#78909C"

            if item.get("is_gps"):
                items_controls.append(
                    build_gps_widget(item, label_color, preview_color, is_mayday)
                )
            elif item.get("is_geocoded"):
                items_controls.append(
                    build_geocoded_widget(item, section["id"], couleur,
                                          label_color, preview_color,
                                          TV_KEYS.get(champ, champ))
                )
            elif item.get("is_counter"):
                items_controls.append(
                    build_counter_widget(item, section["id"], couleur,
                                          label_color, preview_color)
                )
            elif item.get("options_from_symptoms"):
                items_controls.append(
                    build_symptom_radio_widget(item, section["id"], couleur,
                                                label_color, preview_color)
                )
            elif "options" in item:
                items_controls.append(
                    build_radio_widget(item, section["id"], couleur,
                                        label_color, preview_color,
                                        item["options"], TV_KEYS.get(champ))
                )
            else:
                items_controls.append(
                    build_text_widget(item, section["id"], couleur, is_mayday,
                                       TV_KEYS.get(champ))
                )

        body_bg = "#3B0000" if is_mayday else "#112240"

        if is_mayday:
            header_content = ft.Row(
                controls=[
                    ft.Icon(ft.Icons.RADIO, color="#FFFFFF", size=18),
                    ft.Text(section["titre"], size=13,
                            weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text("SECOURS", size=10,
                                        weight=ft.FontWeight.BOLD, color="#B71C1C"),
                        bgcolor="#FFCDD2",
                        border_radius=ft.BorderRadius(4, 4, 4, 4),
                        padding=ft.Padding(6, 2, 6, 2),
                    ),
                ],
                spacing=8,
            )
        else:
            header_content = ft.Text(section["titre"], size=13,
                                      weight=ft.FontWeight.BOLD, color="#FFFFFF")

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=header_content,
                        bgcolor=couleur,
                        border_radius=ft.BorderRadius(8, 8, 0, 0),
                        padding=ft.Padding(14, 10, 14, 10),
                    ),
                    ft.Container(
                        content=ft.Column(controls=items_controls, spacing=4),
                        bgcolor=body_bg,
                        border_radius=ft.BorderRadius(0, 0, 8, 8),
                        padding=ft.Padding(14, 12, 14, 12),
                    ),
                ],
                spacing=0,
            ),
            margin=ft.Padding(0, 0, 0, 10),
        )

    # ─── Prévisualisation ────────────────────────────────────────────────────
    def generer_trame(e):
        lignes = [f"=== {trame['titre']} ===\n"]
        for section in trame["sections"]:
            lignes.append(f"\n{section['titre']}")
            for item in section["items"]:
                champ_key = item["champ"].upper()

                if item.get("is_gps"):
                    valeur = gps_fields[item["champ"]].value.strip() or "[ ... ]"
                elif item.get("is_counter"):
                    fkey   = f"{section['id']}_{item['champ']}"
                    valeur = str(counters[fkey]["value"])
                elif item.get("options_from_symptoms") or "options" in item:
                    fkey   = f"{section['id']}_{item['champ']}"
                    valeur = radios[fkey]["value"] or "[ ... ]"
                else:
                    fkey   = f"{section['id']}_{item['champ']}"
                    f      = fields.get(fkey)
                    valeur = (f.value.strip() if (f and f.value.strip())
                              else item.get("placeholder", "[ ... ]"))

                texte = item["texte"].replace(f"__{champ_key}__", valeur)
                lignes.append(f"  -> {texte}")

        def on_close(ev):
            page.pop_dialog()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("Trame complete", color=COULEUR_TEXTE,
                          weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "\n".join(lignes),
                                size=12, color=COULEUR_TEXTE, selectable=True,
                            ),
                            bgcolor="#0A1628",
                            border_radius=ft.BorderRadius(8, 8, 8, 8),
                            padding=ft.Padding(12, 12, 12, 12),
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=420,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Fermer", color=COULEUR_ACCENT),
                    on_click=on_close,
                ),
            ],
            bgcolor="#112240",
            shape=ft.RoundedRectangleBorder(radius=12),
        ))

    # ─── Layout ──────────────────────────────────────────────────────────────
    return ft.Column(
        controls=[
            en_tete_page("Trame d'appel aux secours", trame["sous_titre"]),

            ft.Container(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.MIC, color="#FFFFFF", size=22),
                            ft.Text(
                                "Remplissez les champs puis lisez lentement au telephone",
                                size=12, color="#FFFFFF", expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor="#1565C0",
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(14, 10, 14, 10),
                ),
                padding=ft.Padding(16, 0, 16, 10),
            ),

            ft.Container(
                content=ft.Column(
                    controls=[build_section(s) for s in trame["sections"]],
                    spacing=0,
                ),
                padding=ft.Padding(16, 0, 16, 8),
            ),

            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PREVIEW, color="#FFFFFF", size=20),
                            ft.Text("Previsualiser la trame complete",
                                    size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ],
                        spacing=10, tight=True,
                    ),
                    bgcolor=COULEUR_ACCENT,
                    on_click=generer_trame,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding(16, 14, 16, 14),
                    ),
                    expand=True,
                ),
                padding=ft.Padding(16, 0, 16, 20),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
