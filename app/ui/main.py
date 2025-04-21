import streamlit as st
from page_prompts import render_prompts_page, initialize_session_state
from page_cards import render_cards_page

st.set_page_config(layout="wide")

menu = st.sidebar.radio("Menu", ["Cards", "Prompts"])

if menu == "Prompts":
    initialize_session_state()
    render_prompts_page()
elif menu == "Cards":
    render_cards_page()
