import streamlit as st
from page_prompts import render_prompts_page

st.set_page_config(layout="wide")

menu = st.sidebar.radio("Menu", ["Cards", "Prompts"])

if menu == "Prompts":
    render_prompts_page()
#elif menu == "Cards":
#    page_cards.render_cards_page()  