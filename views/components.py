"""
Composants UI réutilisables – compatibles Flet 0.85
"""
import flet as ft

# ─── Palette ────────────────────────────────────────────────────────────────
COULEUR_DANGER  = "#D32F2F"
COULEUR_URGENCE = "#FF6F00"
COULEUR_OK      = "#2E7D32"
COULEUR_FOND    = "#0A1628"
COULEUR_CARTE   = "#112240"
COULEUR_ACCENT  = "#00B4D8"
COULEUR_TEXTE   = "#E8F4FD"
COULEUR_SUBTIL  = "#8BA3BC"
COULEUR_NAVBAR  = "#0D1F3C"
COULEUR_LIGNE   = "#1E3A5F"


def border_all(width: float, color: str) -> ft.border.Border:
    """Crée un border uniforme (ft.border.all() absent en 0.85)."""
    s = ft.border.BorderSide(width, color)
    return ft.border.Border(left=s, top=s, right=s, bottom=s)


def carte(content: ft.Control, padding_val: int = 16) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=COULEUR_CARTE,
        border_radius=ft.BorderRadius(12, 12, 12, 12),
        padding=ft.Padding(padding_val, padding_val, padding_val, padding_val),
    )


def badge_urgence(niveau: str) -> ft.Container:
    config = {
        "critique": (COULEUR_DANGER, "CRITIQUE"),
        "urgent":   (COULEUR_URGENCE, "URGENT"),
        "normal":   (COULEUR_OK, "NORMAL"),
    }
    couleur, label = config.get(niveau, (COULEUR_SUBTIL, niveau.upper()))
    return ft.Container(
        content=ft.Text(label, size=10, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        bgcolor=couleur,
        border_radius=ft.BorderRadius(4, 4, 4, 4),
        padding=ft.Padding(6, 2, 6, 2),
    )


def separateur() -> ft.Divider:
    return ft.Divider(height=1, color=COULEUR_LIGNE)


def en_tete_page(titre: str, sous_titre: str = "") -> ft.Container:
    controls = [
        ft.Text(titre, size=22, weight=ft.FontWeight.BOLD, color=COULEUR_TEXTE),
    ]
    if sous_titre:
        controls.append(ft.Text(sous_titre, size=12, color=COULEUR_SUBTIL))
    return ft.Container(
        content=ft.Column(controls=controls, spacing=4, tight=True),
        padding=ft.Padding(16, 16, 16, 8),
    )


def numero_etape(num: int, couleur: str = COULEUR_ACCENT) -> ft.Container:
    return ft.Container(
        content=ft.Text(str(num), size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        bgcolor=couleur,
        border_radius=ft.BorderRadius(20, 20, 20, 20),
        width=32,
        height=32,
        alignment=ft.Alignment(0, 0),
    )
