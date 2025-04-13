import streamlit as st
import requests
import pandas as pd

API_URL = 'http://localhost:8000'

if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False
if 'show_delete_form' not in st.session_state:
    st.session_state.show_delete_form = False
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'edit_prompt_data' not in st.session_state:
    st.session_state.edit_prompt_data = None

def prompt_form(prompt=None):
    name = st.text_input('Prompt Name', value=prompt['name'] if prompt else "")
    prompt = st.text_area('Prompt Text', value=prompt['text'] if prompt else "")
    return name, prompt

def prompt_modifier_form(mod=None):
    nome = st.text_input('Prompt Modifier Name', key='mod_name', value=mod['name'] if mod else "")
    texto = st.text_area('Prompt Modifier Text', key='mod_text', value=mod['text'] if mod else "")
    return nome, texto

def render_prompt_section():
    st.header('🔧 Prompt Manager')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        listar = st.button('📋 List prompts')
    with col2:
        if st.button('➕ Create a new prompt'):
            st.session_state.show_create_form = True
    with col3:
        if st.button('✏️ Edit prompt'):
            st.session_state.show_edit_form = True
    with col4:
        if st.button('🗑️ Delete prompt'):
            st.session_state.show_delete_form = True

    if listar:
        with st.expander('Prompt List', expanded = True):
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
            if st.button('💾 Save new prompt'):
                response = requests.post(f'{API_URL}/prompts', json={"name": name, "prompt": prompt})
                if response.ok:
                    st.success('✅ Prompt was sucessfully created')
                    st.session_state.show_create_form = False
                else:
                    st.error('❌ Error creating the prompt')

    if st.session_state.show_edit_form:
        with st.expander('✏️ Edit Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to edit')
            if prompt_id:
                response = requests.get(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    name, prompt = prompt_form(response.json())
                    if st.button('💾 Save Changes'):
                        update = {'name': name, 'text': prompt}
                        response = requests.put(f'{API_URL}/prompts/{prompt_id}', json=update)
                        if response.ok:
                            st.success('✅ Prompt updated!')
                        else:
                            st.error('❌ Error updating prompt')
                else:
                    st.error('❌ Prompt was not found')

    if st.session_state.show_delete_form:
        with st.expander('🗑️ Delete Prompt', expanded=True):
            prompt_id = st.text_input('Prompt ID to delete')
            if st.button('🚨 Confirm exclusion'):
                response = requests.delete(f'{API_URL}/prompts/{prompt_id}')
                if response.ok:
                    st.success('✅ Prompt deleted')
                else:
                    st.error('❌ Error deleting the prompt')
                st.session_state.show_delete_form = False

def render_prompts_page():
    st.title('Manage Prompts')
    render_prompt_section()
    st.markdown("---")