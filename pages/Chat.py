import streamlit as st
import random
import time
from datetime import datetime
from Homepage import streamlit_logout
import redis
from streamlit_autorefresh import st_autorefresh
import json



print('Loading chat page')
def pushMessagesInSession(idroom:str, timed=False):
    #Questo metodo, data un room ID, ottiene i messaggi di quella room, li formatta e li inserisce nella sessione.

    #Non potendo utilizzare i JSON su redis devo ricreare qualcosa di simile con Python
    # Ogni messaggio deve essere messages = [{timestamp:43499490, mittente:'pippo',messaggio:'ciao'},...]
    if timed:
        messages = st.session_state.r.zrange(f"st:room:*{idroom}", 0, -1, withscores=True)
        # I messaggi delle timed chats prendono dalle room con "*id1:id2".
    else:
        messages = st.session_state.r.zrange(f"st:room:{idroom}", 0, -1, withscores=True)

    messages = list(messages)
    messages = [list(message) for message in messages]
    messages = [[message[0], datetime.fromtimestamp(message[1])] for message in messages]
    formatted_messages = [{'timestamp':message[1].strftime("%d/%m/%Y, %H:%M"), 'mittente':message[0].split(':')[0],'text':message[0].split(':')[1]} for message in messages]
    #print(formatted_messages)
    # Tutto sto ambaradam mi crea una lista di dizionari [{mess1},{mess2},{mess3}]. Ogni dizionario è un messaggio ben formattato e facilmente accessibile.

    st.session_state['chat'] = formatted_messages 
    # Pusho i messaggi nella session state. 

if 'user' in st.session_state:
    # Se l'user è loggato:
    with st.sidebar:
        f"Logged in as **{st.session_state['user']}**"

        # Recupero la lista di amici in modo da poter recuperare gli idroom. 
        friendList = st.session_state.r.hgetall(f"st:friendList:{st.session_state.user}")

        # Ottengo lo status
        if st.session_state['status'] == '1':
            f":red[Do not disturb ⛔]"
        else:
            f":green[Available for chat ✅] "
            
        # Questo hget mi fa tornare la friendlist, che altro non è che un dizionario. Pippo = {amico1 : chatroomID1, amico2 : chatroomID2}s
        selection = st.selectbox(label='Select who you wanna chat with.', options=friendList, index=None)
        if selection:
            clearChat = st.button(label=f'Clear chat with {selection}')
            # Pulsante per pulire le chat che appare solo se è selezionato un amico con cui chattare
            if clearChat:
                st.session_state.r.delete(f'st:room:{friendList[selection]}')
                pushMessagesInSession(friendList[selection])
                # Se viene pigiato il messaggio deleto la chat dal DB di redis e ricarico i messaggi. 

        timedChat = st.toggle(label=f'*Timed chat* 💣')
        if timedChat and selection:
            pushMessagesInSession(friendList[selection], timed=True)
        # Se è attivo il toggle per pushare i messaggi allora li recupero da una timed chat.
                
        st.sidebar.refresh_checkbox = st.toggle(label=':rainbow[**"Live" updates**]')
        logout_button = st.sidebar.button(label=':orange[Logout]', key='asjsdajks')
        # Pulsanti per ottenere i messaggi in tempo reale e per il logout button

    if logout_button:
        streamlit_logout()
        st.switch_page('Homepage.py')
    # Se effettui un logout vieni redirectato alla homepage. 
    
else:
    st.info('Please Login from the Home page and try again.')
    st.switch_page('Homepage.py')   
    # Solito redirect se non sei loggato.

if timedChat and selection:
    st.title(f":red[Timed Chat] with {selection} ⏲️")
    'Timed messages last only 60 seconds.'
elif selection:
    st.title(f'Chat with :rainbow[{selection}]')
else:
    st.title('Chat')

if not selection and not friendList:
    'You have no friends. Add one from the friend page to start chatting.'
    st.image('pages/sadpepe.gif')
    st.page_link('pages/Friends.py', label=':blue[**Switch to friends page.**]')
elif not selection:
    st.warning('Select a friend to start chatting.')


def stream_data(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.025)


st.session_state['queue'] = []
def my_handler(message):
        print(message['data'])
        message_dict = json.loads(message['data'])
        #{"davidino:tes4": 1719671080.2790027} struttura in entrata
        #{timestamp:43499490, mittente:'pippo',messaggio:'ciao'} struttura da ottenere
        formatted_message = [{'timestamp':datetime.fromtimestamp(v).strftime("%d/%m/%Y, %H:%M"), 'mittente':k.split(':')[0],'text':k.split(':')[1]} for k,v in message_dict.items()]
        formatted_message = formatted_message[-1]
        print(formatted_message)
        if formatted_message not in st.session_state['queue']:
            st.session_state['queue'].append(message)
        
        with st.chat_message('user' if formatted_message['mittente']==st.session_state.user else formatted_message['mittente']):
            st.write_stream(stream_data(f"**{formatted_message['mittente']}** *:gray[{formatted_message['timestamp']}:]* "+formatted_message['text']))

# PubSub Stuff
pub = st.session_state.r.pubsub()

if selection:
    # Se selezioni un amico carica i messaggi nella sessione usando pushMessagesInSession()
    if timedChat:
        pushMessagesInSession(f"{friendList[selection]}", timed=True)
        #friendList[selection] è l'idroom
    else:
        pushMessagesInSession(friendList[selection])


    # Questo ciclo va visualizzare i messaggi sullo schermo
    for message in st.session_state.chat:        
        with st.chat_message('user' if message['mittente']==st.session_state.user else message['mittente']):
            #sto IF serve a far cambiare l'icona del mittente. L'user loggato avrà un'icona personalizzata, così da renderlo distinguibile.
            if not timedChat:
                mess = st.markdown(f"**{message['mittente']}** *:gray[{message['timestamp']}:]* "+message['text'])    
            else:
                mess = st.markdown(f":red[**{message['mittente']}**] *:gray[{message['timestamp']}:]* "+message['text'])    



# Accept user input
if prompt := st.chat_input("What is up my man?"):
    if st.session_state.r.get(f"st:dnd:user:{selection}")=='1':
        st.error(f"{selection} non vuole essere disturbato.")
        # Se l'utente al quale stiamo scrivendo è su Do not disturb non riusciremo ad inserire un messaggio nella chat.
    else:
        if not timedChat and selection:
            st.session_state.r.zadd(f'st:room:{friendList[selection]}', {f"{st.session_state.user}:{prompt}" : time.time()})
        # Questa parte appende il messaggio nello z set della chatroom quando l'utente scrive qualcosa.
            pushMessagesInSession(friendList[selection])
        # Refresho la lista dei messaggi
            message_to_publish = json.dumps({f"{st.session_state.user}:{prompt}" : time.time()})
            st.session_state.r.publish(friendList[selection], json.dumps({f"{st.session_state.user}:{prompt}" : time.time()}))
            st.rerun()
        # Faccio un rerun se viene inviato un nuovo messaggio così da aggiornare la chat.
        elif timedChat and selection:
            st.session_state.r.zadd(f'st:room:*{friendList[selection]}', {f"{st.session_state.user}:{prompt}" : time.time()})
            st.session_state.r.expire(f'st:room:*{friendList[selection]}', 60)
            pushMessagesInSession(f"{friendList[selection]}", timed=True)
            message_to_publish = json.dumps({f"{st.session_state.user}:{prompt}" : time.time()})
            st.session_state.r.publish("*"+friendList[selection], message_to_publish )
            st.rerun()


if not st.sidebar.refresh_checkbox:
    pub.unsubscribe()
    print('Unsuscribed to Pub')
if st.sidebar.refresh_checkbox and selection:
    if timedChat:
        pub.subscribe(**{"*"+friendList[selection]: my_handler})
    else:
        pub.subscribe(**{friendList[selection]: my_handler})
    while True:
        time.sleep(0.5)
        pub.get_message()



    