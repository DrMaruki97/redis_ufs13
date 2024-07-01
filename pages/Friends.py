import streamlit as st
from Homepage import streamlit_logout
import pandas as pd
import time

# Page config
st.set_page_config(
    page_title="Friends",
    page_icon="🔥",
)


def userList(pattern):
    # mi serve una lista di username per il widget della ricerca
    return [i for i in st.session_state.r.smembers("sys:user_list") if i.startswith(pattern) and i!=st.session_state.user]

print('app load test')
         
if 'user' in st.session_state:
    print('debug sidebar first load')
# Se l'utente è loggato:
    with st.sidebar:
        f"Currently logged in as **{st.session_state['user']}**"
        print('debug sidebar load')
        if st.session_state['status'] == '1':
            f":red[Do not disturb ⛔]"
        else:
            f":green[Available for chat ✅] "
    logout_button = st.sidebar.button(label=':orange[Logout]')
    # Questi codici servono ad aggiungere le robe nella sidebar.

    if logout_button:
        streamlit_logout()
        st.switch_page('Homepage.py')
    # Se l'utente effettua il logout dal pulsante viene switchata la pagina a quella del login.
else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Homepage.py')
    # Questa parte di codice fa switchare la pagina a quella del login se qualcuno prova ad accedere a /friends.py senza essere loggato

# Questa parte di codice mi permette di ottenere la lista amici dell'utente loggato.
try:
    friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
    print('debug hget')
except:
    friends = []
    print('debug friends')


# con hgetall ottengo la friendlist dell'utente loggato (un hash) in modo da creare un dataframe con gli amici e le loro informazioni
friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
friends_df['Status'] = [st.session_state.r.get(f"st:dnd:user:{friend}") for friend in friends]
friends_df['Status'] = friends_df['Status'].replace(to_replace='0', value='Available')
friends_df['Status'] = friends_df['Status'].replace(to_replace='1', value='Do not disturb')
friends_df['RoomID'] = [friends[friend] for friend in friends]
# creo un dataframe da quel dizionario
friends_df['Select'] = [False for friend in friends]
# creo una colonna con valori True o False per ogni amico nella friendlist. Serve per poterli rimuovere. 


st.title('Search a user')
default_label = 'Type a username, even if partial.'
friend = st.text_input(label=default_label)
selected_friends = []
col1, col2 = st.columns([7,3])
with col1:
    if not friends:
        'It seems like you have no friends.'
        st.image(image='pages/pepecry.gif')
    # Se non hai amici faccio visualizzare un pepe che piange
    elif friends:
        'Your current friendlist'
        friends_df = st.data_editor(friends_df, hide_index=True)
        #Trasformo il dataframe in un dataframe editabile. Così posso selezionare quali utenti rimuovere
with col2:
    # Metto tutti i pulsanti nella seconda colonna
    selected_friends = [user for user in friends_df[friends_df['Select']==True]['User']] if friends else []
    add_button = st.button(label='Add a friend', use_container_width=True)
    search_button = st.button(label='Search', use_container_width=True)
    conf_remove = st.button(label=f'Remove {selected_friends} user from friendlist', use_container_width=True)
    get_user_list = st.button(label='Get full user base', use_container_width=True)
if conf_remove and selected_friends:
    st.session_state.r.hdel(f"st:friendList:{st.session_state.user}", *selected_friends)
    # Se il pulsante di conferma per la rimozione degli amici viene schiacciato E ci sono amici da rimuovere allora manda un hdel
    st.success('Removed your buddies.')
    st.rerun()


st.divider()
# una linea. Sotto mostro i risultati delle ricerche ------------

def add_friend(friend_to_add):
    idroom = [int(st.session_state.r.get('id_user:'+friend_to_add)), int(st.session_state.r.get('id_user:'+st.session_state.user))]
    idroom.sort()
    idroom = ':'.join([str(id) for id in idroom])
    st.session_state.r.hset(f"st:friendList:{st.session_state.user}", friend_to_add, idroom)

# Roba per aggiungere gli amici 
if search_button and friend:
    st.title('Search results')
    resultList = userList(pattern=friend)
    [f"{i}" for i in resultList]
    if len(resultList)==0:
        st.write('There are no users by that name.')
        st.image('pages/pepewhat.png')

if add_button:
    if st.session_state.r.exists('user:'+friend) and friend != st.session_state.user:
        idroom = [int(st.session_state.r.get('id_user:'+friend)), int(st.session_state.r.get('id_user:'+st.session_state.user))]
        idroom.sort()
        idroom = ':'.join([str(id) for id in idroom])
        # Questo mi serve a creare un idroom dell'amico che si è aggiunto. Per crearlo semplicemente accosto gli id dei due user, mettendo prima il piu' piccolo.
        # Esempio. Pippo ha id=1. Paperino ha id=2. Se Paperino aggiunge Pippo l'idroom sarà 1:2.
        # Per creare questo id faccio un doppio get degli id dei due utenti, li inserisco in una lista, la ordino ed unisco gli elementi con :

        st.session_state.r.hset(f"st:friendList:{st.session_state.user}", friend, idroom)
        friends = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")
        friends_df = pd.DataFrame({'User':friends.keys() for friend in friends})
        st.success(f'Great! You added {friend}')
        st.sidebar.image('pages/pepedance.gif')
        time.sleep(1)
        st.rerun()
        # Se viene schiacciato il pulsante per aggiungere un amico viene controllato se quell'utente esistçe effetivamente. 
        # Se esiste viene aggiunto nella hash lista amici

    else: 
        st.error("User simply ain't there buddy")
if get_user_list:
    [i for i in st.session_state.r.smembers("sys:user_list")]

