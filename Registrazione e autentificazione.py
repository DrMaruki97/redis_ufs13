import redis
from conn import connect


def inserimento():
    while True:
        username = input("Inserisci un nome utente: ")
        pwd = input("Inserisci un password utente: ")
        if 4 < len(pwd) < 17 and len(username) < 20:
            break
    return [username, pwd]

def hash_password(pwd):
    # Aggiungi un salt fisso
    salt = "42"
    # Calcola l'hash della password con il salt
    hashed_pwd = hash(pwd + salt)
    return hashed_pwd

# Creiamo una funzione di registrazione utente
def signup(lista):

    # Facciamo in modo di non salvare in bianco la password
    username = lista[0]
    if not r.exists(username):
        pwd = lista[1]
        pwd_hash = hash_password(pwd)

        # Creiamo istanza redis per l'utente
        r.set("user:" + username, pwd_hash)

        # Creiamo un id utente
        id_user = r.incr("id_utente")

        # Creiamo istanza redis per id utente
        r.set("id_utente:" + username, id_user)



# Creiamo una funzione di identificazione
def login(lista):
    username = lista[0]
    pwd = lista[1]
    # Controlliamo l'esistenza dell'utente
    if r.exists(username):
        # Hashamo la pwd inserita
        check_pwd = hash_password(pwd)
        stored_pwd = r.get("user:" + username)

        if stored_pwd == check_pwd:
            return True
        return login(inserimento())



# Creiamo una funzione per aggiungere un amico nella rubrica
def add_friend(user, friend):
    if not r.exists("user:" + friend):
        return False
    else:
        # Se esiste, aggiungiamo l'amico alla rubrica
        r.sadd("rubrica:" + user, friend )

def remove_friend(user, friend):
    if not r.exists("user:" + friend):
        return False
    else:
        # Se esiste, rimuoviamo l'amico alla rubrica
        r.scard("rubrica:" + user, friend )
def stampa_rubrica(user):
    # Stampiamo la rubrica
    for friend in r.smembers("rubrica:" + user):
        print(friend)


r = connect()
signup(inserimento())
login(inserimento())
add_friend(input("Inserisci il tuo user"), input("Inserisci il tuo friend"))
stampa_rubrica(input("Inserisci il tuo user"))