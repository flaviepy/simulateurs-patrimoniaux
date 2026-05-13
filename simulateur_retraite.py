# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:47:59 2026

@author: ryanj
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulateur retraite",
    page_icon="📈",
    layout="wide"
)

st.title("Simulateur d’épargne retraite")
st.write(
    "Ce simulateur permet d’estimer le capital constitué à la retraite "
    "à partir d’un capital initial, d’un effort mensuel et d’un rendement moyen."
)

st.sidebar.header("Paramètres du simulateur")

age_actuel = st.sidebar.number_input(
    "Âge actuel",
    min_value=18,
    max_value=70,
    value=38,
    step=1
)

capital_depart = st.sidebar.number_input(
    "Capital de départ (€)",
    min_value=0,
    value=50,
    step=100
)

effort_mensuel = st.sidebar.number_input(
    "Effort mensuel (€)",
    min_value=0,
    value=200,
    step=50
)

age_retraite = st.sidebar.slider(
    "Âge de départ à la retraite",
    min_value=60,
    max_value=70,
    value=64,
    step=1
)

esperance_vie = st.sidebar.slider(
    "Espérance de vie",
    min_value=70,
    max_value=120,
    value=90,
    step=1
)

profil = st.sidebar.selectbox(
    "Profil de risque",
    ["Prudent", "Équilibré", "Dynamique", "Offensif"]
)

rendements = {
    "Prudent": 0.03,
    "Équilibré": 0.05,
    "Dynamique": 0.07,
    "Offensif": 0.09
}

rendement_annuel = rendements[profil]

rendement_rente = st.sidebar.slider(
    "Rendement phase de rente (%)",
    min_value=1,
    max_value=8,
    value=4,
    step=1
) / 100

st.subheader("Paramètres sélectionnés")

col1, col2, col3 = st.columns(3)

col1.metric("Âge actuel", f"{age_actuel} ans")
col2.metric("Départ à la retraite", f"{age_retraite} ans")
col3.metric("Espérance de vie", f"{esperance_vie} ans")

col4, col5, col6 = st.columns(3)

col4.metric("Capital de départ", f"{capital_depart:,.0f} €")
col5.metric("Effort mensuel", f"{effort_mensuel:,.0f} €")
col6.metric("Rendement annuel estimé", f"{rendement_annuel*100:.1f} %")

# Calcul de la durée d'épargne
duree_epargne = age_retraite - age_actuel

# Conversion du rendement annuel en rendement mensuel
rendement_mensuel = (1 + rendement_annuel) ** (1/12) - 1

# Nombre total de mois
nb_mois = duree_epargne * 12

# Initialisation
capital = capital_depart

# Listes pour le graphique
liste_capital = []
liste_annees = []

# Boucle de capitalisation
for mois in range(nb_mois):
    capital = (capital + effort_mensuel) * (1 + rendement_mensuel)

    # Stockage annuel
    if mois % 12 == 0:
        age = age_actuel + mois / 12
        liste_capital.append(capital)
        liste_annees.append(age)

capital_retraite = capital

st.subheader("Résultats")

st.metric(
    "Capital estimé à la retraite",
    f"{capital_retraite:,.0f} €"
)

# Somme totale réellement investie
somme_investie = capital_depart + effort_mensuel * nb_mois

# Gains générés par les intérêts
interets_generes = capital_retraite - somme_investie

st.subheader("Comparaison entre l’épargne versée et le capital obtenu")

# Rente sans consommer le capital
rente_sans_capital = capital_retraite * rendement_rente / 12

# Durée de retraite
duree_retraite = esperance_vie - age_retraite

# Nombre de mois de retraite
mois_retraite = duree_retraite * 12

# Rente en consommant le capital
r = (1 + rendement_rente) ** (1/12) - 1

rente_avec_capital = (
    capital_retraite * r
    / (1 - (1 + r) ** (-mois_retraite))
)

fig, ax = plt.subplots(figsize=(3.5,2.8))

categories = ["Somme investie", "Capital obtenu"]
valeurs = [somme_investie, capital_retraite]

ax.bar(
    categories,
    valeurs,
    color="#0f3359"
)
ax.set_ylim(0, max(valeurs) * 1.15)

ax.set_title("Effet des intérêts composés")
ax.set_ylabel("Montant (€)")

# Ajouter les valeurs au-dessus des barres
for i, valeur in enumerate(valeurs):
    ax.text(
        i,
        valeur,
        f"{valeur:,.0f} €",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

col_graphique, col_texte = st.columns([2,1])

with col_graphique:
    st.pyplot(fig, use_container_width=False)

with col_texte:

    st.subheader("Estimation des rentes")

    st.metric(
        "Sans consommer le patrimoine",
        f"{rente_sans_capital:,.0f} €/mois"
    )

    st.metric(
        "En consommant le patrimoine",
        f"{rente_avec_capital:,.0f} €/mois"
    )

    st.caption(
        "La seconde estimation suppose une consommation progressive du capital jusqu’à l’espérance de vie choisie."
    )

st.write(
    f"Dans ce scénario, l’utilisateur investit réellement **{somme_investie:,.0f} €** "
    f"et obtient un capital estimé de **{capital_retraite:,.0f} €** à la retraite."
)

st.write(
    f"Les intérêts composés représenteraient donc environ **{interets_generes:,.0f} €**."
)