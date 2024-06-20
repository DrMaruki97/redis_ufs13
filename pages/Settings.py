# Questa pagina viene utilizzata per cambiare le impostazioni utente

import streamlit as st

if 'user' in st.session_state:
    f"{st.session_state['user']}"
else:
    st.info('Please Login from the Home page and try again.')
    st.stop()