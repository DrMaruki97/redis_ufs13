import redis

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
    return hash_value


"""LOGIN e REGISTRAZIONE"""


def start_form():
    while True:
        username = input("Inserisci il tuo username: ")
        pwd = input("Inserisci la password: ")
        if 4 < len(pwd) < 17 and len(username) < 20:
            break
    return username, pwd


def sign_up(username, pwd,r):
    if not r.exists(f"user:{username.lower()}"):
        c = r.set(f"user:{username.lower()}", hash_pwd(pwd))
        if c:
            id = r.incrby("sys:id_user", 1)
            c = r.set(f"id_usr:{username}", id)
    else:
        return False  # utente già esistente
    return c   # True o False in base all'esito della set dell'id


def login(username, pwd,r):
    if r.exists(f"user:{username.lower()}"):
        if hash_pwd(pwd) == r.get("user:" + username.lower()):
            return True, r.get(f"id_usr:{username}"), username  # se login ha successo, restituisce true e id e usrname
        else:
            return False  # pwd sbagliata
    else:
        return False  # utente non esiste


"""GESTIONE AMICI"""


def manage_friends(friend):
    global current_user

    if r.exists("user:" + friend.lower()):
        r.sadd(f"contacts:+{current_user}", friend)
        return True
    return False


def rm_friends(friend):
    global current_user

    if r.exists("user:" + friend.lower()):
        r.srem(f"contacts:+{current_user}", friend)
        return True
    return False


"""RICERCA PARZIALE UTENTE: f. che permette la ricerca di un username anche parzialmente ("davi" invece che davidino),
restituisce una lista che è il risultato della ricerca basata sull'username in input"""


def select_user(username_da_cercare):
    lista_utenti = []
    i = 0
    cursor, utenti = r.scan(0, match=f"user:*")
    for utente in utenti:
        if username_da_cercare.lower() in utente[5:]:
            lista_utenti.append(f"{i + 1}: {key[5:]}")
            i = i + 1
    return lista_utenti
    # viene restituita una lista che è il risultato della ricerca, l'utente deve poter selezionare quello giusto


current_user = "reactor"

""" CHAT A TEMPO: Viene usata una chiave con scadenza temporale impostata dall'utente"""


def timed_chat(user, friend, duration_chat):
    if r.exists(f"room:{user}:{friend}"):
        r.zadd(f"t_room:{user}:{friend}")
        r.expire(f"t_room:{user}:{friend}", time=duration_chat)
        print(f"La chat è iniziata e sarà disponibile per {duration_chat} secondi")


def change_psw(user,psw,r):
    return r.set(user.lower(),hash_pwd(psw))
        
