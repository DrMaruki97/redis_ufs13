import streamlit as st
from Login import streamlit_logout
import pandas as pd

if 'user' in st.session_state:
# Se l'utente è loggato:
    st.title('Friends')
    st.sidebar.text(f"Currently logged in as {st.session_state['user']}")
    if st.session_state['status'] == '1':
        st.sidebar.text(f"Do not disturb ⛔")
    else:
        st.sidebar.text(f"Available for chat ✔️ ")
    logout_button = st.sidebar.button(label='Logout')
    # Questi codici servono ad aggiungere le robe nella sidebar.

    if logout_button:
        streamlit_logout()
        st.switch_page('Login.py')
    # Se l'utente effettua il logout dal pulsante viene switchata la pagina a quella del login.
else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Login.py')
    # Questa parte di codice fa switchare la pagina a quella del login se qualcuno prova ad accedere a /friends.py senza essere loggato

# Questa parte di codice mi permette di ottenere la lista amici dell'utente loggato.
friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
# con hgetall creo un dizionario degli amici
friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
# creo un dataframe da quel dizionario
friends_df['Remove'] = [False for friend in friends]
# creo una colonna con valori True o False per ogni amico nella friendlist. Serve per poterli rimuovere. 

if not friends:
    st.write('***Your current friendlist:***')
    'It seems like you have no friends.'
    st.image(image='pages/pepecry.gif')
    # Se non hai amici faccio visualizzare un pepe che piange
else:
    friends_df = st.data_editor(friends_df, hide_index=True)
    #Trasformo il dataframe in un dataframe editabile. Così posso selezionare quali utenti rimuovere

    conf_remove = st.button(label='Remove from friendlist')
    # Pulsante per rimuovere
    friends_to_be_removed = [user for user in friends_df[friends_df['Remove']==True]['User']]
    # Che comando! Semplicemente creo una lista degli utenti da rimuovere estrapolando gli utenti sul quale ho selezionato remove nel dataframe editabile
    if conf_remove and friends_to_be_removed:
        st.session_state.r.hdel(f"st:friendList:{st.session_state.user}", *friends_to_be_removed)
        # Se il pulsante di conferma per la rimozione degli amici viene schiacciato E ci sono amici da rimuovere allora manda un hdel
        st.success('Removed your buddies.')
        st.rerun()

st.divider()
# una linea ------------

st.title('Add a friend')
friend = st.text_input(label='Type your friend username')
add_button = st.button(label='Add a friend')
# Roba per aggiungere gli amici 
if add_button:
    if st.session_state.r.exists('user:'+friend):
        st.session_state.r.hset(f"st:friendList:{st.session_state.user}", friend, 'temp')
        friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
        friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
        st.success(f'Added {friend}')
        st.rerun()
        # Se viene schiacciato il pulsante per aggiungere un amico viene controllato se quell'utente esiste effetivamente. 
        # Se esiste viene aggiunto nella hash lista amici

    else: 
        st.error("User simply ain't there buddy")






