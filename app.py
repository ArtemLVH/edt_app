import streamlit as st
import pandas as pd
from pathlib import Path
import os

# --- Config ---
st.set_page_config(page_title="Emploi du temps", layout="wide")

# --- Secrets & verrou d'édition ---
APP_PASSWORD = st.secrets.get("APP_PASSWORD") or os.environ.get("APP_PASSWORD") or "edt2025"

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    with st.form("lock_form", clear_on_submit=False):
        pwd = st.text_input("Mot de passe", type="password", placeholder="••••••")
        ok = st.form_submit_button("Déverrouiller")

    if ok:
        if pwd == APP_PASSWORD:
            st.session_state.unlocked = True
            st.success("Édition déverrouillée ✅")
            try:
                st.rerun()
            except Exception:
                st.experimental_rerun()
        else:
            if pwd:  # pas d'erreur si champ vide
                st.error("Mot de passe incorrect ❌")

    st.stop()

# --- App principale ---
st.title("📅 Emploi du temps interactif — Semaine par semaine")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
heures = [f"{h:02d}h-{h+1:02d}h" for h in range(8, 21)]  # 8h–20h

def blank_df():
    return pd.DataFrame("", index=heures, columns=jours)

def load_week(name: str) -> pd.DataFrame:
    f = DATA_DIR / f"{name}.csv"
    if f.exists():
        return pd.read_csv(f, index_col=0)
    return blank_df()

def save_week(name: str, df: pd.DataFrame):
    f = DATA_DIR / f"{name}.csv"
    df.to_csv(f, encoding="utf-8", index=True)

def get_palette(preset: str):
    palettes = {
        "Pastel (clair)": {
            "CM": "#DCEBFF", "TD": "#C7DDFF", "Cours": "#DCEBFF",
            "BU": "#DDF7E6", "Projet": "#DDF7E6",
            "Musculation": "#EADDFE",
            "Club photo": "#FFE0EC", "Court métrage": "#FFDDB8",
            "RU": "#FFF4B8"
        },
        "Vif (contrasté)": {
            "CM": "#8EC5FF", "TD": "#62B0FF", "Cours": "#8EC5FF",
            "BU": "#7FE3A4", "Projet": "#7FE3A4",
            "Musculation": "#C39BFF",
            "Club photo": "#FFA8C8", "Court métrage": "#FFB36A",
            "RU": "#FFD659"
        },
        "Gris + accents": {
            "CM": "#E6EEF8", "TD": "#D3E2F6", "Cours": "#E6EEF8",
            "BU": "#E6F5EC", "Projet": "#E6F5EC",
            "Musculation": "#EEE6F8",
            "Club photo": "#FCE6EE", "Court métrage": "#FBEBD8",
            "RU": "#FFF5CC"
        }
    }
    return palettes.get(preset, palettes["Pastel (clair)"])

def colored_html_table(df: pd.DataFrame, palette_name: str, font_px: int) -> str:
    palette = get_palette(palette_name)

    def cell_style(text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            return "background:#f5f5f5;color:#111;"
        for key, col in palette.items():
            if key.lower() in text.lower():
                return f"background:{col};color:#111;font-weight:600;"
        return "background:#FFFFFF;color:#111;"

    css = f'''
    <style>
    table.edt{{border-collapse:collapse;width:100%;font-family:system-ui;font-size:{font_px}px;}}
    table.edt th,table.edt td{{border:1px solid #ddd;padding:8px;text-align:center;vertical-align:middle}}
    table.edt thead th{{position:sticky;top:0;background:#fafafa;color:#111}}
    table.edt tbody th{{position:sticky;left:0;background:#fafafa;color:#111}}
    </style>
    '''

    html = [css, "<table class='edt'>"]
    html.append("<thead><tr><th>Heure</th>")
    for j in df.columns:
        html.append(f"<th>{j}</th>")
    html.append("</tr></thead><tbody>")
    for idx, row in df.iterrows():
        html.append(f"<tr><th>{idx}</th>")
        for val in row:
            style = cell_style(val)
            safe = (val if isinstance(val, str) else "")
            html.append(f"<td style='{style}'>{safe}</td>")
        html.append("</tr>")
    html.append("</tbody></table>")
    return "".join(html)

# --- UI ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    week_name = st.text_input("Nom de la semaine", value="Semaine 1")
    palette = st.selectbox("Palette de couleurs", ["Pastel (clair)", "Vif (contrasté)", "Gris + accents"])
    font_px = st.slider("Taille du texte (px)", 10, 20, 14, 1)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("➕ Créer semaine vide"):
            save_week(week_name, blank_df())
            st.success(f"Semaine '{week_name}' créée.")
    with col_b:
        if st.button("📂 Charger"):
            st.session_state["df"] = load_week(week_name)
            st.success(f"Semaine '{week_name}' chargée.")
    with col_c:
        if st.button("💾 Sauvegarder"):
            save_week(week_name, st.session_state.get("df", blank_df()))
            st.success(f"Semaine '{week_name}' sauvegardée.")

if "df" not in st.session_state:
    st.session_state["df"] = load_week("Semaine 1")

st.subheader("Édition")
edited = st.data_editor(
    st.session_state["df"],
    use_container_width=True,
    num_rows="fixed",
    hide_index=False,
)
st.session_state["df"] = edited

st.subheader("Vue esthétique (couleurs par activité)")
st.markdown(colored_html_table(edited, palette, font_px), unsafe_allow_html=True)

with st.expander("🎨 Légende des couleurs"):
    st.markdown(
        "- **Bleu**: Cours/CM/TD  \n"
        "- **Vert**: BU / Projet  \n"
        "- **Violet**: Musculation  \n"
        "- **Orange**: Court métrage / Club photo  \n"
        "- **Jaune**: RU (repas)"
    )

