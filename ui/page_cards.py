import requests
import streamlit as st

API_URL = 'http://localhost:8000'


@st.cache_data
def get_prompts():
    """Retrieves the prompts from the database, adding it to cache"""
    response = requests.get(f'{API_URL}/prompts/?limit=50')
    if response.ok:
        prompts = response.json().get('prompts', [])
        return prompts, {prompt['name']: prompt for prompt in prompts}
    return [], {}


@st.cache_data
def get_prompt_modifiers():
    """Retrieves the prompt modifiers from the database, adding it to cache"""
    response = requests.get(f'{API_URL}/prompt-modifiers/?limit=50')
    if response.ok:
        modifiers = response.json().get('prompt_modifiers', [])
        return modifiers, {modifier['name']: modifier for modifier in modifiers}
    return [], {}


def initialize_text_areas_keys():
    """Initializes default values for text areas in session_state"""
    defaults = {
        'words': '',
        'deck': '',
        'tag': '',
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def reset_ptompt_and_modifiers_cache():
    """Resets the cache"""
    get_prompts.clear()
    get_prompt_modifiers.clear()


def render_text_area(label: str, state_key: str, allow_space: bool = True):
    """Generic function to render the text form with session_state
    If allow_space is False, spaces are removed automatically.
    """
    text = st.text_area(label, key=state_key)

    if not allow_space:
        replaced_text = text.replace(' ', '')
        if replaced_text != text:
            st.session_state[state_key] = replaced_text
            st.warning('The space between the words was automatically removed')
        return st.session_state[state_key]

    return text


def update_text_input(source_key: str, target_key: str):
    """Generic function that updades the session_state given a key"""
    st.session_state[target_key] = st.session_state[source_key]


def render_input_form():
    """Renders the input form"""
    st.subheader('🔤 Data input')

    render_text_area('Words (comma separated)', 'words')
    words_text = st.session_state['words']
    words = [w.strip() for w in words_text.split(',') if w.strip()]

    if st.button('🔄 Reload Prompts and Modifiers'):
        reset_ptompt_and_modifiers_cache()

    with st.spinner('Loading prompts and modifiers...'):
        _, prompt_dict = get_prompts()
        _, modifier_dict = get_prompt_modifiers()

    if not prompt_dict:
        st.warning('No prompts found. Please create at least one prompt before generating cards.')
        st.stop()
    
    prompt_names = list(prompt_dict.keys())
    modifier_names = list(modifier_dict.keys())

    selected_prompt_name = st.selectbox('Prompt', options=prompt_names)
    selected_modifier_name = st.multiselect('Prompt Modifiers', options=modifier_names)

    selected_prompt_obj = prompt_dict[selected_prompt_name]
    selected_modifier_obj = [modifier_dict[name] for name in selected_modifier_name]

    return words, selected_prompt_obj, selected_modifier_obj


def generate_cards(
    words: list[str],
    prompt_data: dict,
    modifiers_data: list[dict],
) -> list[dict[str, str]]:
    """Makes the requisition to the API to generate the cards"""
    data = {
        'words': words,
        'prompt': prompt_data['prompt'],
        'modifier': [modifier['prompt'] for modifier in modifiers_data] if modifiers_data else [],
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
                st.markdown(f'**Card {i + 1}**')
                st.markdown(f'**Word:** {card["word"]}')
                st.markdown(f'**Front:** {card["front"]}')
                st.markdown(f'**Back:** {card["back"]}')
                st.divider()

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                render_text_area('Deck', 'deck', allow_space=False)
            with col2:
                render_text_area('Tag', 'tag', allow_space=False)
            with col3:
                render_export_button()
    else:
        st.info('No card was generated yet.')


def render_export_button():
    """Renders the anki export button"""
    if st.button('📤 Export Cards to Anki', use_container_width=True):
        deck = st.session_state.get('deck', '')
        tag = st.session_state.get('tag', '')

        export_payload = {'cards': st.session_state.generated_cards, 'deck': deck, 'tag': tag}

        export_response = requests.post(f'{API_URL}/export-cards/', json=export_payload)

        if export_response.ok:
            st.success('✅ Cards successfully exported.')
            st.session_state.generated_cards = []  # Clear cards after export
        else:
            st.error('❌ Error exporting the cards.')


def render_cards_page():
    st.title('📇 Flashcards Generator')

    initialize_text_areas_keys()

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
