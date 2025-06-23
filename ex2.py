import plotly.graph_objects as go
import streamlit as st


def plot_depenses_region_plotly(region, df_budget, df_dep, df_lin, df_energie):
    annees = df_budget.iloc[:, 0]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=annees, y=df_budget.iloc[:, 1],
        mode='lines+markers', name='Budget',
        line=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=annees, y=df_dep.iloc[:, 1],
        mode='lines+markers', name='Dépenses',
        line=dict(color='blue'), marker=dict(symbol='cross')
    ))

    fig.add_trace(go.Scatter(
        x=annees, y=df_lin.iloc[:, 1],
        mode='lines+markers', name='Dépenses linéaires',
        line=dict(color='green'), marker=dict(symbol='circle')
    ))

    fig.add_trace(go.Scatter(
        x=annees, y=df_energie.iloc[:, 1],
        mode='lines+markers', name='Dépenses énergie',
        line=dict(color='black'), marker=dict(symbol='x')
    ))

    fig.update_layout(
        title=f"Comparaison budgets & dépenses – {region}",
        xaxis_title="Années",
        yaxis_title="EUR",
        height=500,
        legend_title="Catégorie",
        hovermode="x unified"
    )

    return fig

