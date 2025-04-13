import pandas as pd
import requests
import streamlit as st

API_URL = 'http://localhost:8000'

if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False
if 'show_delete_form' not in st.session_state:
    st.session_state.show_delete_form = False
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'show_create_modifier_form' not in st.session_state:
    st.session_state.show_create_modifier_form = False
if 'show_delete_modifier_form' not in st.session_state:
    st.session_state.show_delete_modifier_form = False
if 'show_edit_modifier_form' not in st.session_state:
    st.session_state.show_edit_modifier_form = False



def prompt_form(prompt=None):
    name = st.text_input('Prompt Name', value=prompt['name'] if prompt else "")
    text = st.text_area('Prompt Text', value=prompt['prompt'] if prompt else "")
    return name, text


def prompt_modifier_form(mod=None):
    name = st.text_input('Prompt Modifier Name', key='mod_name', value=mod['name'] if mod else "")
    text = st.text_area('Prompt Modifier Text', key='mod_text', value=mod['prompt'] if mod else "")
    return name, text


def render_prompt_section():
    st.header('🔧 Prompt Manager')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        list = st.button('📋 List prompts', key= 'list_prompts_button')
    with col2:
        if st.button('➕ Create prompt', key = 'create_prompt_button'):
            st.session_state.show_create_form = True
    with col3:
        if st.button('✏️ Edit prompt', key='edit_prompt_button'):
            st.session_state.show_edit_form = True
    with col4:
        if st.button('🗑️ Delete prompt', key='delete_prompt_button'):
            st.session_state.show_delete_form = True

    if list:
        with st.expander('Prompt List', expanded=True):
            response = requests.get(f'{API_URL}/prompts/?limit=50')
            if response.ok:
                data = response.json()
                prompts = data.get('prompts', [])
                if prompts:
                    df = pd.DataFrame(prompts)
                    st.dataframe(df[['id', 'name', 'prompt']], use_container_width=True)
                else:
                    st.info('No prompt was recorded')
            else:
                st.error('Error acessing prompts')

    if st.session_state.show_create_form:
        with st.expander('➕ New Prompt', expanded=True):
            name, prompt = prompt_form()
            if st.button('💾 Save new prompt', key= 'save_new_prompt_button'):
                response = requests.post(f'{API_URL}/prompts', json={"name": name, "prompt": prompt})
                if response.ok:
                    st.success('✅ Prompt was sucessfully created')
                    st.session_state.show_create_form = False
                else:
                    st.error('❌ Error creating the prompt')

    if st.session_state.show_edit_form:
        with st.expander('✏️ Edit Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to edit', key= 'edit_prompt_id_input')
            if prompt_id:
                response = requests.get(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    name, prompt = prompt_form(response.json())
                    if st.button('💾 Save changes', key= 'save_edit_prompt_button'):
                        update = {'name': name, 'prompt': prompt}
                        response = requests.put(f'{API_URL}/prompts/{prompt_id}', json=update)
                        print(response)
                        if response.ok:
                            st.success('✅ Prompt updated!')
                        else:
                            st.error('❌ Error updating prompt')
                else:
                    st.error('❌ Prompt was not found')

    if st.session_state.show_delete_form:
        with st.expander('🗑️ Delete Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to delete', key= 'delete_prompt_id_input')
            if st.button('🚨 Confirm exclusion', key= 'confirm_exclusion_button'):
                response = requests.delete(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    st.success('✅ Prompt deleted')
                else:
                    st.error('❌ Error deleting the prompt')
                st.session_state.show_delete_form = False


def render_prompt_modifiers_page():
    st.header('🔧 Prompt Modifier Manager')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        listar = st.button('📋 List prompt modifiers', key= 'list_prompt_modifiers_button')
    with col2:
        if st.button('➕ Create prompt modifier', key= 'create_prompt_modifier_button'):
            st.session_state.show_create_modifier_form = True
    with col3:
        if st.button('✏️ Edit prompt modifier', key= 'edit_prompt_modifier_button'):
            st.session_state.show_edit_modifier_form = True
    with col4:
        if st.button('🗑️ Delete prompt modifier', key= 'delete_prompt_modifier_button'):
            st.session_state.show_delete_modifier_form = True

    if listar:
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

    if st.session_state.show_create_modifier_form:
        with st.expander('➕ New Prompt Modifier', expanded=True):
            name, prompt = prompt_modifier_form()
            if st.button('💾 Save new prompt modifier', key= 'save_new_prompt_modifier_button'):
                response = requests.post(f'{API_URL}/prompt-modifiers', json={"name": name, "prompt": prompt})
                if response.ok:
                    st.success('✅ Prompt modifier was sucessfully created')
                    st.session_state.show_create_modifier_form = False
                else:
                    st.error('❌ Error creating the prompt modifier')

    if st.session_state.show_edit_modifier_form:
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

    if st.session_state.show_delete_modifier_form:
        with st.expander('🗑️ Delete Prompt Modifier', expanded=True):
            prompt_modifier_id = st.text_input('Prompt modifier ID to delete', key= 'delete_prompt_modifier_id_input')
            if st.button('🚨 Confirm exclusion', key= 'confirm_delete_prompt_modifier_button'):
                response = requests.delete(f'{API_URL}/prompt-modifiers/{prompt_modifier_id}')
                if response.ok:
                    st.success('✅ Prompt modifier deleted')
                else:
                    st.error('❌ Error deleting the prompt modifier')
                st.session_state.show_delete_modifier_form = False


def render_prompts_page():
    st.title('Manage Prompts')
    render_prompt_section()
    st.markdown("---")
    render_prompt_modifiers_page()
