import streamlit as st
import requests

API_URL = 'http://localhost:8000'

def get_prompts():
    response = requests.get(f"{API_URL}/prompts/?limit=50")
    if response.ok:
        prompts = response.json().get('prompts', [])
        return prompts, {p['name']: p for p in prompts}
    return [], {}

def get_prompt_modifiers():
    response = requests.get(f'{API_URL}/prompt-modifiers/?limit=50')
    if response.ok:
        modifiers = response.json().get('prompt_modifiers', [])
        return modifiers, {m['name']: m for m in modifiers}
    return [], {}

def render_input_form():
    st.subheader('🔤 Data input')

    words = st.text_area('Words')

    _, prompt_dict = get_prompts()
    _, modifier_dict = get_prompt_modifiers()

    prompt_names = list(prompt_dict.keys())
    modifier_names = list(modifier_dict.keys())

    selected_prompt_name = st.selectbox('Prompt', options=prompt_names)
    selected_modifier_name = st.selectbox('Prompt Modifier', options=modifier_names)

    selected_prompt_obj = prompt_dict[selected_prompt_name]
    selected_modifier_obj = modifier_dict[selected_modifier_name]

    return words, selected_prompt_obj, selected_modifier_obj

def generate_cards(words, selected_prompt, selected_modifier):
    """Makes the requisition to the API to generate the cards"""
    dados = {
        'words': [words],
        'prompt': selected_prompt['prompt'],
        'modifier': [selected_modifier['prompt']] if selected_modifier else []
    }

    response = requests.post(f'{API_URL}/generate-cards/', json=dados)
    print(dados)
    if response.ok:
        return response.json()
    return []

def render_generated_cards():
    """Renders the cards generated"""
    if 'generated_cards' in st.session_state and st.session_state.generated_cards:
        for i, card in enumerate(st.session_state.generated_cards):
            with st.container():
                st.markdown(f"**Card {i + 1}**")
                st.markdown(f"**Front:** {card['front']}")
                st.markdown(f"**Back:** {card['back']}")
                st.divider()

        render_export_button()
    else:
        st.info('No card was generated yet.')

def render_export_button():
    """Renders the anki export button"""
    if st.button('📤 Export Cards to Anki', use_container_width=True):
        export_response = requests.post(
            f'{API_URL}/export-cards',
            json={'cards': st.session_state.generated_cards}
        )
        if export_response.ok:
            st.success('✅ Cards successfully exported.')
            st.session_state.generated_cards = []  # Clear cards after export
        else:
            st.error('❌ Error exporting the cards.')

def render_cards_page():
    st.title('📇 Flashcards Generator')

    col1, col2 = st.columns([1, 2])

    with col1:
        palavras, prompt_selecionado, modifier_selecionado = render_input_form()

        if st.button('⚡ Generate cards'):
            generated_cards = generate_cards(palavras, prompt_selecionado, modifier_selecionado)

            if generated_cards:
                st.session_state.generated_cards = generated_cards
                st.success('✅ Cards successfully generated')
            else:
                st.error('❌ Error generating cards.')

    with col2:
        render_generated_cards()