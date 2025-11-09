# app_steamlit.py

import streamlit as st
from user_input import show_calculator
from food_wiki import show_food_wiki

st.set_page_config(page_title="Nutrition Therapy App", layout="centered")

# Defines the tabs
tab1, tab2, tab3 = st.tabs(["Nutrition Calculator", "Food Wiki", "Ingredient Scanner"])

with tab1:
    show_calculator()

with tab2: # UNCOMMENTED: Display the Food Wiki content
    show_food_wiki()

# with tab3:
    # show_OCR_scanner()