import plotly.graph_objects as go
import streamlit as st

# Exemple : regions = ["IDF", "PACA", ...]
for i, region in enumerate(regions):
    df_budget = dfs_public[i]
    df_dep = dfs_menages[i]
    df_lin = dfs_menages_lin[i]
    df_energie = dfs_energie[i]

    annees = df_budget.iloc[:, 0]
    y_budget = df_budget.iloc[:, 1]
    y_dep = df_dep.iloc[:, 1]
    y_lin = df_lin.iloc[:, 1]
    y_energie = df_energie.iloc[:, 1]

    with st.expander(f"📍 {region}"):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=annees, y=y_budget, mode='lines+markers',
            name='Budget', line=dict(color='red')
        ))

        fig.add_trace(go.Scatter(
            x=annees, y=y_dep, mode='lines+markers',
            name='Dépenses', line=dict(color='blue'), marker=dict(symbol='cross')
        ))

        fig.add_trace(go.Scatter(
            x=annees, y=y_lin, mode='lines+markers',
            name='Dépenses linéaires', line=dict(color='green'), marker=dict(symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=annees, y=y_energie, mode='lines+markers',
            name='Dépenses énergie', line=dict(color='black'), marker=dict(symbol='x')
        ))

        fig.update_layout(
            title=f"Comparaison des budgets et dépenses - {region}",
            xaxis_title="Années",
            yaxis_title="EUR",
            height=500,
            legend_title="Catégorie",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)
