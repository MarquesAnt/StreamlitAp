import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

BASE_PATH = "data/"

def plot_emissions(filepath):
    df = pd.read_csv(filepath)

    if df.shape[1] < 15:
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

def charger_depenses_public(regions, dossiers, date, solution, base_path="data/"):
    dataframes = []
    for region, dossier in zip(regions, dossiers):
        try:
            if region == "LNAQ":
                path = os.path.join(base_path, f"Batiment/LNAQ/{solution}_Building_NAQ_{date}/depenses_public_Building_NAQ.csv")
            elif region == "LNMD":
                path = os.path.join(base_path, f"Batiment/LNMD/{solution}_Building_NMD_{date}/depenses_public_Building_NMD.csv")
            else:
                path = os.path.join(base_path, f"Batiment/{region}/{dossier}/depenses_public_Building_{region}.csv")
            df = pd.read_csv(path, sep=";")
            df["region"] = region
            dataframes.append(df)
        except Exception as e:
            st.warning(f"⚠️ Erreur pour {region}: {e}")
    return dataframes

# Interface Streamlit
st.title("📊 Visualisation des émissions carbone et des dépenses publiques")

nom_dossier = st.text_input("🗂️ Nom du dossier (ex: output_folder_name3)")
date_input = st.text_input("📅 Date ou suffixe (ex: 2024-06-18)")

# --------------------------
# Bloc 1 : Émissions carbone
# --------------------------
if nom_dossier and date_input:
    emissions_path = os.path.join(BASE_PATH, f"{nom_dossier}_main_{date_input}", "emissions.csv")
    if os.path.exists(emissions_path):
        st.success(f"✅ Fichier trouvé : {emissions_path}")
        plot_emissions(emissions_path)
    else:
        st.error(f"❌ Fichier non trouvé : {emissions_path}")

# --------------------------
# Bloc 2 : Dépenses publiques (comparatif multi-régions)
# --------------------------
st.markdown("---")
st.header("📉 Dépenses publiques comparées entre régions")

regions = ["AURA", "BFC", "BRE", "COR", "CVL", "GRE", "HDF", "IDF", "LNAQ", "LNMD", "OCC", "PACA", "PDL"]
dossier_input = st.text_area("🗂️ Un dossier par ligne (13 au total)", value="\n".join(regions))
dossiers = dossier_input.splitlines()
solution = st.text_input("📦 Nom de la solution (ex: output_folder_name3)")

if st.button("Charger les dépenses publiques"):
    if len(dossiers) != len(regions):
        st.error("⚠️ Le nombre de dossiers ne correspond pas au nombre de régions.")
    else:
        dfs = charger_depenses_public(regions, dossiers, date_input, solution)

        # Vérification et fusion
        try:
            # On suppose que toutes les régions ont la même colonne d'années (colonne 0)
            merged_df = pd.DataFrame()
            for df in dfs:
                region = df["region"].iloc[0]
                year_col = df.columns[0]
                value_col = df.columns[1]  # On prend la 2e colonne (ex: "Dépenses")
                df_region = df[[year_col, value_col]].copy()
                df_region.columns = ["Année", region]
                if merged_df.empty:
                    merged_df = df_region
                else:
                    merged_df = pd.merge(merged_df, df_region, on="Année", how="outer")

            merged_df = merged_df.sort_values("Année")
            merged_df = merged_df.set_index("Année")

            st.subheader("📊 Dépenses publiques par région (comparées)")
            st.line_chart(merged_df)

        except Exception as e:
            st.error(f"Erreur lors du traitement des données fusionnées : {e}")
