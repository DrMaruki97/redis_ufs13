import redis
import time


"""CONNESSIONE AL DB: f. decode_responses = le richieste sono decodificate, restituisce r variabile database"""


def connect():
    r = redis.Redis(
    host='redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=16230,
    password='y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL',
    decode_responses=True
    )
    return r


"""ALGORITMO DI HASH: semplice algoritmo che maschera le password, ogni carattere della pwd viene sostituito da un
numero che è diviso per la lunghezza della pw, e sommato al valore precedente dell'hash per 31"""


def hash_pwd(pwd):
    hash_value = 89
    for char in pwd:
        hash_value = (hash_value * 31 + ord(char)) // len(pwd)
    print(f"L'hash della stringa '{pwd}' è: {hash_value}")  # Perchè questo print? da eliminare
    return hash_value


"""LOGIN e REGISTRAZIONE: Si inseriscono in input stringhe per usr e pwd valide, se usr non esiste viene creata l'
utenza, se invece esiste viene verificata la password inserita (se ne calcola l'hash e la si confronta con la hash 
salvata nel database), in entrambi i casi viene restituito lo {username}. Se la pwd è sbagliata, restituisce False"""


def login_signup():
    while True:
        username = input("Inserisci il tuo username: ")  # Io dividerei le due funzionalità
        pwd = input("Inserisci la password: ")
        if 4 < len(pwd) < 17 and len(username) < 20:
            break
    if not r.exists(username):
        r.set("user:" + username, hash_pwd(pwd))
        return username
    else:
        if hash_pwd(pwd) == r.get("user:" + username):
            return username
        else:
            return False


"""Funzione che cicla finché non viene fatto un LOGIN corretto o un SIGNUP (registrazione corretta)"""


def current_user():
    while not login_signup():
        login_signup()
    return login_signup()


"""GESTIONE AMICI: f. in input username dell'utente e dell'amico. 
Se usr amico esiste, si verifica se esiste la chat tra i due,
se esiste si chiede se per caso si vuole rimuoverlo dagli amici e archiviare la chat, si attende si o no (s/n).
Se viene risposto "s" ovvero sì, la chat viene archiviata (tecnicamente cambia nome da "room" a "archive"). 
Altrimenti se non esiste una chat con l'utente, viene creata la chat (vuota).
Se usr amico non esiste viene restituito msg di errore"""


def manage_friends(user, friend):
    if r.exists("user:"+friend):
        if r.exists("room:"+user+":"+friend):
            response = input("Sei già amico con l'utente, desideri rimuoverlo e archiviare la chat? (s/n)")
            if response == "s" or "S":
                r.rename("room:"+user+":"+friend, "archive:"+user+":"+friend)
            else:
                pass
        else:
            timestamp = time.time()
            r.zadd("room:" + user + ":" + friend, {"member": timestamp})
    else:
        print("L'utente non esiste")


"""STAMPA LISTA CONTATTI e INIZIALIZZARE CHAT: Viene usato SCAN molto più efficiente di smembers o keys, cerca le chiavi
 con un determinato pattern, in questo caso il pattern delle chat: "room:user1:user2" se esiste la room,
significa che sono amici, viene offerta la possibilità di scegliere la room per iniziare la chat e viene restituita 
la chiave associata alla room f.e. "room:reactor:davidino" """


def select_friend(user):
    cursor, keys = r.scan(0, match=f"room:{user}:*")
    for index, key in enumerate(keys):
        print(f"{index}: {key[len(user)+6:]}")
    select = int(input("Inserire numero utente desiderato"))
    try:
        return keys[select]
    except Exception as e:
        return False, print("Hai inserito un numero non valido")


"""RICERCA PARZIALE UTENTE: f. che permette la ricerca di un username anche parzialmente ("davi" invece che davidino),
e che una volta selezionato automaticamente permette di aggiungerlo agli amici (tecnicamente inizializzare la chat),
oppure rimuoverlo se è gia amico. Non usare direttamente la funzione manage_friends ma questa PRIMA"""


def select_user(user):
    ricerca = input("Inserire il nome utente da cercare: ")
    lista_utenti = []
    i = 0
    cursor, keys = r.scan(0, match=f"user:*")
    for key in keys:
        if ricerca in key[5:]:
            lista_utenti.append(f"{i+1}: {key[5:]}")
            i = i +1
    print(lista_utenti)
    select = int(input("Inserire numero utente desiderato: "))
    try:
        return manage_friends(user, lista_utenti[select-1][3:])
    except Exception as e:
        return False, print("Hai inserito un numero non valido")

""" CHAT A TEMPO: Viene usata una chiave con scadenza temporale impostata dall'utente"""
def timed_chat(user, friend):
    if r.exists("room:"+user+":"+friend):
        print("Scegli quando far durare la chat a scomparsa: ")
        print("Scegli 1 : 10 minuti")
        print("Scegli 2 : 30 minuti")
        print("Scegli 3 : 1 ora")
        scelta_durata = int(input("Inserisci un numero da 1 a 3: "))

        if scelta_durata == "1":
            durata_chat = 10 * 60
        elif scelta_durata == "2":
            durata_chat = 30 * 60
        elif scelta_durata == "3":
            durata_chat = 60 * 60
        else:
            return False

        r.expire("room:"+user+":"+friend, time=durata_chat)
        print(f"La chat è iniziata e sarà disponibile per {durata_chat/60} secondi")
    else:
        return False




# Le prossime sono da sistemare perchè userei una bitmap(forse dovremmo reintrodurre gli id)

'''Funziona che controlla lo stato DnD di un utente (che dobbiamo aver creato e settato a 0 durante la registrazione/ settato a 0
durante un login) e ritorna la variabile dnd che avrà valore 0\\1'''

"""Siate liberi di testare"""
r = connect()
select_user("reactor")

def check_dnd(user):
    dnd = r.get(f'DnD:{user}')
    return dnd


def change_dnd(user,dnd):
    try:
        if dnd:
            r.set(f'DnD:{user}',0)
        else:
            r.set(f'DnD:{user}',1)
        return True
    except:
        return False

