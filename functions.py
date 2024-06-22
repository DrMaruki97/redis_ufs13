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
    print(f"L'hash della stringa '{pwd}' è: {hash_value}")
    return hash_value


"""LOGIN e REGISTRAZIONE: Si inseriscono in input stringhe per usr e pwd valide, se usr non esiste viene creata l'
utenza, se invece esiste viene verificata la password inserita (se ne calcola l'hash e la si confronta con la hash 
salvata nel database), in entrambi i casi viene restituito lo {username}. Se la pwd è sbagliata, restituisce False"""


def login_signup():
    while True:
        username = input("Inserisci il tuo username: ")
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
            r.zadd("room:" + user + ":" + friend, {"member": 10.3})
    else:
        print("L'utente non esiste")


"""STAMPA LISTA CONTATTI: Viene usato SCAN molto più efficiente di smembers o keys, cerca le chiavi con un determinato
pattern, in questo caso il pattern delle chat: "room:user1:user2" se esiste la room, significa che sono amici"""


def print_friends(user):
    cursor, keys = r.scan(0, match=f"room:{user}:*")
    for key in keys:
        print(key[len(user)+6:])

""" CHAT A TEMPO: Viene usata una chiave con scadenza temporale impostata dall'utente"""
def timed_chat(user, friend, duration_chat):
    if r.exists("room:"+user+":"+friend):
        duration_chat = int(input("Inserisci la durata della chat: "))
        r.expire("room:"+user+":"+friend, time=duration_chat)
        print(f"La chat è iniziata e sarà disponibile per {duration_chat} secondi}")




"""Siate liberi di testare"""