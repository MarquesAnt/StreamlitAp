import streamlit as st
import pandas as pd
import os

BASE_PATH = "data/"

def load_csv_auto(filepath):
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(filepath, sep=sep)
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    return pd.read_csv(filepath)

def find_csv_files_recursive(base_folder):
    csv_paths = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

# Fonction d'affichage personnalisée (à compléter plus tard)
def plot_custom_graphs(df, filename):
    st.subheader(f"📄 {filename}")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            st.line_chart(df[col], use_container_width=True)
    else:
        st.info("Aucune colonne numérique détectée.")

# Interface utilisateur
st.title("📊 Visualisation automatique d'un dossier de sortie")

folder_input = st.text_input("Nom du dossier principal (relatif à /data/)")

if folder_input:
    folder_path = os.path.join(BASE_PATH, folder_input)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        st.success(f"✅ Dossier trouvé : {folder_path}")

        csv_files = find_csv_files_recursive(folder_path)
        if not csv_files:
            st.warning("Aucun fichier CSV trouvé dans ce dossier ou ses sous-dossiers.")
        else:
            for file_path in csv_files:
                try:
                    df = load_csv_auto(file_path)
                    plot_custom_graphs(df, os.path.relpath(file_path, BASE_PATH))
                except Exception as e:
                    st.error(f"Erreur lors du chargement de {file_path} : {e}")
    else:
        st.error("Dossier introuvable. Vérifie le nom que tu as entré.")
