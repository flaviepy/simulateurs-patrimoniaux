# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:12:23 2026

@author: ryanj
"""
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulateur assurance-vie",
    page_icon="📈",
    layout="wide"
)

st.title("Simulateur assurance-vie")

st.write(
    "Ce simulateur permet d’estimer l’évolution d’un capital placé en assurance-vie "
    "à partir d’un capital initial, de versements mensuels et d’un rendement moyen."
)

st.sidebar.header("Paramètres du simulateur")

capital_depart = st.sidebar.number_input(
    "Capital de départ (€)",
    min_value=0,
    value=1000,
    step=500
)

versement_mensuel = st.sidebar.number_input(
    "Versement mensuel (€)",
    min_value=0,
    value=200,
    step=50
)

duree_placement = st.sidebar.slider(
    "Durée de placement (années)",
    min_value=1,
    max_value=40,
    value=20,
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
rendement_mensuel = (1 + rendement_annuel) ** (1/12) - 1

nb_mois = duree_placement * 12
capital = capital_depart

for mois in range(nb_mois):
    capital = (capital + versement_mensuel) * (1 + rendement_mensuel)

capital_final = capital
somme_investie = capital_depart + versement_mensuel * nb_mois
interets_generes = capital_final - somme_investie

st.header("Résultats de la simulation")

col1, col2, col3 = st.columns(3)

col1.metric("Somme investie", f"{somme_investie:,.0f} €")
col2.metric("Capital estimé", f"{capital_final:,.0f} €")
col3.metric("Intérêts générés", f"{interets_generes:,.0f} €")

st.subheader("Comparaison entre l’épargne versée et le capital obtenu")

fig, ax = plt.subplots(figsize=(3.5, 2.8))

categories = ["Somme investie", "Capital obtenu"]
valeurs = [somme_investie, capital_final]

ax.bar(
    categories,
    valeurs,
    color="#0f3359"
)

ax.set_ylim(0, max(valeurs) * 1.15)
ax.set_title("Effet des intérêts composés")
ax.set_ylabel("Montant (€)")

for i, valeur in enumerate(valeurs):
    ax.text(
        i,
        valeur,
        f"{valeur:,.0f} €",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

st.pyplot(fig, use_container_width=False)

st.caption(
    "Cette simulation repose sur un rendement moyen constant. Elle permet de visualiser "
    "l’effet des intérêts composés mais ne constitue pas une prévision certaine."
)