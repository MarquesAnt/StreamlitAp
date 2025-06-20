import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

BASE_PATH = "data/"

def plot_emissions(filepath):
    df = pd.read_csv(filepath)

    if df.shape[1] < 16:
        st.warning("⚠️ Le fichier ne contient pas au moins 15 colonnes.")
        return

    x = df.iloc[:, 0]  # Années
    y_columns = df.columns[1:15]

    st.subheader("📈 Évolution des émissions carbone")
    fig, ax = plt.subplots(figsize=(10, 5))

    for col in y_columns:
        ax.plot(x, df[col], label=col)

    ax.set_xlabel("Année")
    ax.set_ylabel("Émissions carbone")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.set_title("Émissions carbone par région")

    st.pyplot(fig)

# Interface Streamlit
st.title("📊 Visualisation des émissions carbone")

nom_dossier = st.text_input("🗂️ Nom du dossier (ex: output_folder_name3)")
date_input = st.text_input("📅 Date ou suffixe (ex: 2024-06-18)")

if nom_dossier and date_input:
    full_path = os.path.join(BASE_PATH, f"{nom_dossier}_main_{date_input}", "emissions.csv")

    if os.path.exists(full_path):
        st.success(f"✅ Fichier trouvé : {full_path}")
        plot_emissions(full_path)
    else:
        st.error(f"❌ Fichier non trouvé : {full_path}")
