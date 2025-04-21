import pandas as pd
import requests
import streamlit as st

API_URL = 'http://localhost:8000'

def initialize_session_state():
    default_states = {
        'show_create_form': False,
        'show_delete_form': False,
        'show_edit_form': False,
        'show_create_modifier_form': False,
        'show_delete_modifier_form': False,
        'show_edit_modifier_form': False
    }
    for key, default in default_states.items():
        st.session_state.setdefault(key, default)

def prompt_form(prompt=None):
    name = st.text_input('Prompt Name', value=prompt['name'] if prompt else "")
    text = st.text_area('Prompt Text', value=prompt['prompt'] if prompt else "")
    return name, text


def prompt_modifier_form(mod=None):
    name = st.text_input('Prompt Modifier Name', key='mod_name', value=mod['name'] if mod else "")
    text = st.text_area('Prompt Modifier Text', key='mod_text', value=mod['prompt'] if mod else "")
    return name, text

def render_prompt_buttons():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        list_prompts = st.button('📋 List prompts')
    with col2:
        if st.button('➕ Create prompt'):
            st.session_state.show_create_form = True
    with col3:
        if st.button('✏️ Edit prompt'):
            st.session_state.show_edit_form = True
    with col4:
        if st.button('🗑️ Delete prompt'):
            st.session_state.show_delete_form = True
    return list_prompts

def list_prompts():
    with st.expander('Prompt List', expanded=True):
            response = requests.get(f'{API_URL}/prompts/?limit=50')
            if response.ok:
                prompts = response.json().get('prompts', [])
                if prompts:
                    df = pd.DataFrame(prompts)
                    st.dataframe(df[['id', 'name', 'prompt']], use_container_width=True)
                else:
                    st.info('No prompt was recorded')
            else:
                st.error('Error acessing prompts')

def create_prompt():
    with st.expander('➕ New Prompt', expanded=True):
            name, prompt = prompt_form()
            if st.button('💾 Save new prompt', key= 'save_new_prompt_button'):
                response = requests.post(f'{API_URL}/prompts', json={"name": name, "prompt": prompt})
                if response.ok:
                    st.success('✅ Prompt was sucessfully created')
                    st.session_state.show_create_form = False
                else:
                    st.error('❌ Error creating the prompt')

def edit_prompt():
    with st.expander('✏️ Edit Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to edit', key= 'edit_prompt_id_input')
            if prompt_id:
                response = requests.get(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    name, prompt = prompt_form(response.json())
                    if st.button('💾 Save changes', key= 'save_edit_prompt_button'):
                        update = {'name': name, 'prompt': prompt}
                        response = requests.put(f'{API_URL}/prompts/{prompt_id}', json=update)
                        if response.ok:
                            st.success('✅ Prompt updated!')
                        else:
                            st.error('❌ Error updating prompt')
                else:
                    st.error('❌ Prompt was not found')

def delete_prompt():
    with st.expander('🗑️ Delete Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to delete', key= 'delete_prompt_id_input')
            if st.button('🚨 Confirm exclusion', key= 'confirm_exclusion_button'):
                response = requests.delete(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    st.success('✅ Prompt deleted')
                else:
                    st.error('❌ Error deleting the prompt')
                st.session_state.show_delete_form = False

def render_prompt_section():
    st.header('🔧 Prompt Manager')
    if render_prompt_buttons():
        list_prompts()
    if st.session_state.show_create_form:
        create_prompt()
    if st.session_state.show_edit_form:
        edit_prompt()
    if st.session_state.show_delete_form:
        delete_prompt()

def render_prompt_modifier_buttons():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        list_mods = st.button('📋 List prompt modifiers')
    with col2:
        if st.button('➕ Create prompt modifier'):
            st.session_state.show_create_modifier_form = True
    with col3:
        if st.button('✏️ Edit prompt modifier'):
            st.session_state.show_edit_modifier_form = True
    with col4:
        if st.button('🗑️ Delete prompt modifier'):
            st.session_state.show_delete_modifier_form = True
    return list_mods

def list_prompt_modifiers():
    with st.expander('Prompt Modifier List', expanded=True):
            response = requests.get(f'{API_URL}/prompt-modifiers/?limit=50')
            if response.ok:
                data = response.json()
                prompt_modifiers = data.get('prompt_modifiers', [])
                if prompt_modifiers:
                    df = pd.DataFrame(prompt_modifiers)
                    st.dataframe(df[['id', 'name', 'prompt']], use_container_width=True)
                else:
                    st.info('No prompt modifier was recorded')
            else:
                st.error('Error acessing prompt modifiers')

def create_prompt_modifier():
    with st.expander('➕ New Prompt Modifier', expanded=True):
            name, prompt = prompt_modifier_form()
            if st.button('💾 Save new prompt modifier', key= 'save_new_prompt_modifier_button'):
                response = requests.post(f'{API_URL}/prompt-modifiers', json={"name": name, "prompt": prompt})
                if response.ok:
                    st.success('✅ Prompt modifier was sucessfully created')
                    st.session_state.show_create_modifier_form = False
                else:
                    st.error('❌ Error creating the prompt modifier')

def edit_prompt_modifier():
    with st.expander('✏️ Edit Prompt Modifier', expanded=True):
            prompt_modifier_id = st.text_input('Prompt modifier ID to edit', key='edit_prompt_modifier_id_input')
            if prompt_modifier_id:
                response = requests.get(f'{API_URL}/prompt-modifiers/{prompt_modifier_id}')
                if response.ok:
                    name, prompt = prompt_modifier_form(response.json())
                    if st.button('💾 Save changes', key= 'save_edit_prompt_modifier_button'):
                        update = {'name': name, 'prompt': prompt}
                        response = requests.put(f'{API_URL}/prompt-modifiers/{prompt_modifier_id}', json=update)
                        if response.ok:
                            st.success('✅ Prompt modifier updated!')
                        else:
                            st.error('❌ Error updating prompt modifier')
                else:
                    st.error('❌ Prompt modifier was not found')

def delete_prompt_modifier():
    with st.expander('🗑️ Delete Prompt Modifier', expanded=True):
            prompt_modifier_id = st.text_input('Prompt modifier ID to delete', key= 'delete_prompt_modifier_id_input')
            if st.button('🚨 Confirm exclusion', key= 'confirm_delete_prompt_modifier_button'):
                response = requests.delete(f'{API_URL}/prompt-modifiers/{prompt_modifier_id}')
                if response.ok:
                    st.success('✅ Prompt modifier deleted')
                else:
                    st.error('❌ Error deleting the prompt modifier')
                st.session_state.show_delete_modifier_form = False

def render_prompt_modifiers_section():
    st.header('🔧 Prompt Modifier Manager')
    if render_prompt_modifier_buttons():
        list_prompt_modifiers()
    if st.session_state.show_create_modifier_form:
        create_prompt_modifier()
    if st.session_state.show_edit_modifier_form:
        edit_prompt_modifier()
    if st.session_state.show_delete_modifier_form:
        delete_prompt_modifier()

def render_prompts_page():
    initialize_session_state()
    st.title('Manage Prompts')
    render_prompt_section()
    st.markdown("---")
    render_prompt_modifiers_section()
