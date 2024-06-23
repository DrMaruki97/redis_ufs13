import streamlit as st
import redis 

st.set_page_config(
    page_title="Login",
    page_icon="🔥",
)

# Funzione che ti permette di loggare con streamlit
def streamlit_login(user, password, r):
    #prende in entrata user, password e l'oggetto R per la connessione al DB
    if r.exists("user:"+user)==1:
        print('It exists!')
        actualPass = r.get("user:"+ user)
        # se l'utente esiste piglia la password e la confronta con quella inserita dall'utente
        if actualPass==password:
            print('Password Match')
            st.session_state['user'] = user
            st.session_state['status'] = r.get('dnd:user:'+user)
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

# Insert a form in the container
if 'user' not in st.session_state:
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
        st.success("Login successful")
        st.switch_page('pages/Friends.py')
        #se il login è avvenuto metto lo username nella sessione e switcho alla pagina degli amici
    else:
        st.error("Login failed")
  if register_button:
    #Se invece l'utente preferisce registrarsi...
    if not r.exists('user:'+username):
        r.set("user:"+ username, password)
        f"Congratulations, {username}. You're in."
        st.session_state['user'] = username
        st.switch_page('pages/Friends.py')
        # Switcho pagina se la registrazione è andata a buon fine. 
    else:
        'Username already exists.'


if 'user' in st.session_state:
    st.empty()
    st.switch_page('pages/Friends.py')
# Questa parte di codice serve a fare in modo che se sei loggato non puoi accedere alla pagina di login.