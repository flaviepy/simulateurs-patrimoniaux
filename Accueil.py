# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:51:08 2026

@author: ryanj
"""

import streamlit as st

st.set_page_config(
    page_title="Simulateurs Garantis",
    page_icon="💼",
    layout="wide"
)

st.title("Simulateurs Garantis Patrimoine")

st.write(
    "Bienvenue sur l'application de simulation patrimoniale."
)

st.markdown("## Choisir un simulateur")

if st.button("Simulateur retraite"):
    st.switch_page("pages/simulateur_retraite.py")
    
if st.button("Simulateur assurance-vie"):
    st.switch_page("pages/simulateur_assurance_vie.py")