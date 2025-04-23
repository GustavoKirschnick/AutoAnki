import streamlit as st
import requests

API_URL = 'http://localhost:8000'

def get_prompts():
    response = requests.get(f"{API_URL}/prompts/?limit=50")
    if response.ok:
        prompts = response.json().get('prompts', [])
        return prompts, {prompt['name']: prompt for prompt in prompts}
    return [], {}

def get_prompt_modifiers():
    response = requests.get(f'{API_URL}/prompt-modifiers/?limit=50')
    if response.ok:
        modifiers = response.json().get('prompt_modifiers', [])
        return modifiers, {modifier['name']: modifier for modifier in modifiers}
    return [], {}

def render_input_form():
    """Renders the input form"""
    st.subheader('🔤 Data input')

    words = st.text_area('Words')
    words = [w.strip() for w in words.split(',') if w.strip()]

    _, prompt_dict = get_prompts()
    _, modifier_dict = get_prompt_modifiers()

    prompt_names = list(prompt_dict.keys())
    modifier_names = list(modifier_dict.keys())

    selected_prompt_name = st.selectbox('Prompt', options=prompt_names)
    selected_modifier_name = st.multiselect('Prompt Modifiers', options=modifier_names)

    selected_prompt_obj = prompt_dict[selected_prompt_name]
    selected_modifier_obj = [modifier_dict[name] for name in selected_modifier_name]

    return words, selected_prompt_obj, selected_modifier_obj

def generate_cards(words: list[str], prompt_data: dict, modifiers_data: list[dict]) -> list[dict[str,str]]:
    """Makes the requisition to the API to generate the cards"""
    data = {
        'words': words,
        'prompt': prompt_data['prompt'],
        'modifier': [modifier['prompt'] for modifier in modifiers_data] if modifiers_data else []
    }

    response = requests.post(f'{API_URL}/generate-cards/', json=data)

    if response.ok:
        return response.json()
    return []

def render_generated_cards():
    """Renders the cards generated"""
    if 'generated_cards' in st.session_state and st.session_state.generated_cards:
        for i, card in enumerate(st.session_state.generated_cards):
            with st.container():
                st.markdown(f"**Card {i + 1}**")
                st.markdown(f"**Word:** {card['words']}")
                st.markdown(f"**Front:** {card['front']}")
                st.markdown(f"**Back:** {card['back']}")
                st.divider()

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                render_deck_text_input()
            with col2:
                render_tag_text_input()
            with col3:
                render_export_button()
    else:
        st.info('No card was generated yet.')

def render_export_button():
    """Renders the anki export button"""
    if st.button('📤 Export Cards to Anki', use_container_width=True):
        print(st.session_state.generated_cards)
        deck = st.session_state.get('deck', '')
        tag =  st.session_state.get('tag', '')

        export_payload = {
            'cards': st.session_state.generated_cards,
            'deck': deck,
            'tag': tag
        }

        export_response = requests.post(
            f'{API_URL}/export-cards/',
            json=export_payload
        )

        if export_response.ok:
            st.success('✅ Cards successfully exported.')
            st.session_state.generated_cards = []  # Clear cards after export
        else:
            st.error('❌ Error exporting the cards.')

def render_deck_text_input():
    """Contains the deck input field"""
    deck = st.text_area('Deck')
    st.session_state.deck = deck
    return deck

def render_tag_text_input():
    """Contains the tag input field"""
    tag = st.text_area('Tag')
    st.session_state.tag = tag
    return tag

def render_cards_page():
    st.title('📇 Flashcards Generator')

    col1, col2 = st.columns([1, 2])

    with col1:
        words, selected_prompt, selected_modifier = render_input_form()

        if st.button('⚡ Generate cards'):
            generated_cards = generate_cards(words, selected_prompt, selected_modifier)

            if generated_cards:
                st.session_state.generated_cards = generated_cards
                st.success('✅ Cards successfully generated')
            else:
                st.error('❌ Error generating cards.')

    with col2:
        render_generated_cards()