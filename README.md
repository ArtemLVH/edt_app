
# Emploi du temps — Application Streamlit

## Prérequis
- Python 3.9 ou plus
- Internet non requis (appli locale)

## Installation
1) Ouvrez un terminal (PowerShell sous Windows, Terminal sur macOS/Linux)
2) Créez un environnement virtuel (recommandé) :
   - Windows: `python -m venv .venv && .\.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
3) Installez les dépendances :
   `pip install -r requirements.txt`

## Lancer l'app
```
streamlit run app.py
```
Puis ouvrez le lien local affiché (généralement http://localhost:8501).

## Utilisation
- Dans la barre latérale, choisissez un **nom de semaine** (ex: "Semaine 1" ou une date).
- Cliquez **Charger semaine** pour ouvrir, **Sauvegarder semaine** pour enregistrer.
- **Double-cliquez** sur les cellules pour éditer (comme un tableur).
- La section **Vue esthétique** affiche la grille colorée automatiquement par type d'activité.

## Où sont stockées les données ?
Dans le dossier `data/` au format CSV (un fichier par semaine).
