# Questa pagina viene utilizzata per cambiare le impostazioni utente

import streamlit as st
from Login import streamlit_logout
import time

if 'user' in st.session_state:
    st.title('Settings')
    st.sidebar.text(f"Currently logged in as {st.session_state['user']}")
    if st.session_state['status'] == '1':
        st.sidebar.text(f"Do not disturb ⛔")
    else:
        st.sidebar.text(f"Available for chat ✔️ ")

    logout_button = st.sidebar.button(label='Logout')
    if logout_button:
        streamlit_logout()
        st.switch_page('Login.py')
    st.write(f"Hello, **{st.session_state['user']}**")
    # Solita roba per la sidebar


    new_password = st.text_input(label="Choose a new password", placeholder=f'Current password: {st.session_state.r.get("user:"+st.session_state.user)}')
    # mostro la password corrente. chiaramente non è una buona practice ma mi è utile

    DnD = st.toggle("Do not disturb")
    update_button= st.button("Update", type="primary")
    if update_button:
        # Quando viene schiacciato il pulsante di update verifico cosa è selezionato e in base a quello piglia l'if giusto. Bruttissimo, ma funziona.
        if new_password and DnD:
            st.session_state.r.set('user:'+st.session_state.user, new_password)
            st.toast('Changed password!')
            st.session_state.r.set('st:dnd:user:'+st.session_state.user, "1")
            st.error('Activated do not disturb.', icon='⛔')
            st.session_state['status'] = '1'
            time.sleep(1)
            st.rerun()
        elif new_password:
            st.session_state.r.set('user:'+st.session_state.user, new_password)
            st.toast('Changed password!')
            time.sleep(1)
            st.rerun()

        elif DnD: 
            st.session_state.r.set('st:dnd:user:'+st.session_state.user, "1")
            st.toast('Activated do not disturb.', icon='⛔')
            st.session_state['status'] = '1'
            time.sleep(1)
            st.rerun()

        else:
            st.session_state.r.set('st:dnd:user:'+st.session_state.user, "0")
            st.toast('Set status as available', icon='✔️')
            st.session_state['status'] = '0'
            time.sleep(1)
            st.rerun()

        

else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Login.py')
