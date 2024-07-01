import streamlit as st
import redis
from functions import hash_pwd
import time

# Page config
st.set_page_config(
    page_title="Homepage",
    page_icon="🔥",
)

def sign_up(username, pwd):
    if not r.exists(f"user:{username.lower()}"):
        c = r.set(f"user:{username.lower()}", hash_pwd(pwd))
        if c:
            id = r.incrby("sys:id_user", 1)
            r.set(f"id_user:{username.lower()}",id)
            r.sadd(f"sys:user_list", username)
    else:
        return False  # utente già esistente
    return True

# Funzione che ti permette di loggare con streamlit
def streamlit_login(user, password, r):
    if user in ['', ' ']:
        st.error('Invalid credentials.')
        return False
    #prende in entrata user, password e l'oggetto R per la connessione al DB
    if r.exists("user:"+user)==1:
        print('It exists!')
        actualPass = r.get("user:"+ user)
        # se l'utente esiste piglia la password e la confronta con quella inserita dall'utente
        if actualPass==str(hash_pwd(password)):
            print('Password Match')
            st.session_state['user'] = user
            st.session_state['status'] = r.set('st:dnd:user:'+user, '0')
            st.session_state['status'] = '0'
            st.session_state['redirect'] = True
            #se i dati sono corretti inserisce nella sessione di streamlit l'username e lo 'status', ovvero 'disponibile' o 'dnd'
            return True
        else:
            return False

def streamlit_logout():
    del st.session_state['user']
    # il logout semplicemente rimuove l'utente dalla sessione



r = redis.Redis(
    host='redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=16230,
    password='y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL',
    decode_responses=True
    )
st.session_state['r'] = r
#inizializzo l'oggetto per la connesione al database nella pagina principale e poi inserisco questo oggetto nella sessione per renderlo disponibile su tutte le pagine


st.title('🔥 :red[Red]Chat 💬')

# Create an empty container
placeholder = st.empty()

# Se l'user non è loggato compare il form per loggare o registrarsi
if 'user' not in st.session_state:
  st.cache_data.clear()
  login_form = st.form(key='login_form')
  username = login_form.text_input(label='username')
  password = login_form.text_input(label='password', type='password')
  submit_button = login_form.form_submit_button(label='submit')
  register_button = login_form.form_submit_button(label='register')
  #form di login/registrazione

  #se viene schiacciato il pulsante di submit
  if submit_button:
    login = streamlit_login(username, password, r)
    #viene tentato un login
    if login:
        st.session_state['user'] = username
        st.toast("Login successful")
        st.success(f"Congratulations, {username}. You're in.")
        #r.sadd(f"sys:user_list", username)
        st.sidebar.image("pages/pepedance.gif")
        #time.sleep(1)
        st.session_state['user'] = username
        print('I will now attempt redirect')
        time.sleep(1)
        st.rerun()
        #st.switch_page('pages/Friends.py')

        #se il login è avvenuto metto lo username nella sessione e switcho alla pagina degli amici
    else:
        st.error("Login failed")
  if register_button:
    #Se invece l'utente preferisce registrarsi...
    if (username or password) in ['', ' ']:
        st.error('Invalid credentials.') 
    elif not r.exists('user:'+username):
        sign_up(username, password)
        st.session_state['status'] = r.set('st:dnd:user:'+username, '0')
        st.session_state['status'] = '0'
        st.success(f"Congratulations, {username}. You're in.")
        st.sidebar.image("pages/pepedance.gif")
        st.session_state['user'] = username
        time.sleep(1)
        st.rerun()
    else:
        'Username already exists.'

# Se l'user invece è loggato mostro i settings. 
if 'user' in st.session_state:
    st.title('Settings')
    with st.sidebar:
        f"Currently logged in as **{st.session_state['user']}**"
        if st.session_state['status'] == '1':
            f":red[Do not disturb ⛔]"
        else:
            f":green[Available for chat ✅] "

    logout_button = st.sidebar.button(label=':orange[Logout]')
    if logout_button:
        streamlit_logout()
        st.switch_page('Homepage.py')
    st.write(f"Hello, **{st.session_state['user']}**")
    # Solita roba per la sidebar


    new_password = st.text_input(label="Choose a new password", placeholder=f'you better remember it')
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
            st.session_state.r.set('user:'+st.session_state.user, hash_pwd(new_password))
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

        

