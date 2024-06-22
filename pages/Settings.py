# Questa pagina viene utilizzata per cambiare le impostazioni utente

import streamlit as st
from Login import streamlit_logout

if 'user' in st.session_state:
    st.title('Settings')
    logout_button = st.sidebar.button(label='Logout')
    if logout_button:
        streamlit_logout()
        st.switch_page('Login.py')
    st.write(f"Hello, **{st.session_state['user']}**")

    new_password = st.text_input(label="Choose a new password", placeholder=f'Current password: {st.session_state.r.get("user:"+st.session_state.user)}')
    DnD = st.toggle("Do not disturb")
    update_button= st.button("Update", type="primary")
    if update_button:
        st.session_state.r.set('user:'+st.session_state.user, new_password)
        st.success('Updated!')
        

else:
    st.info('Please Login from the Home page and try again.')
    st.stop()
