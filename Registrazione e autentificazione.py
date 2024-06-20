import bcrypt  # libreria per hashing delle pwd
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
def registrazione_utente(lista):

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
def autentificazione_utente(username, pwd):
    while True:
        inserimento()
        # Controlliamo l'esistenza dell'utente
        if r.exists(username):
            hash_password(pwd)
    # Controlliamo, dopo averla recuperata, se la password fornita dall'utente corrisponde a quella memorizzata

    get_pwd_hash = r.get("user:" + username)

    if not bcrypt.checkpw(pwd.encode('utf-8'), get_pwd_hash.encode('utf-8')):
        return "Autentificazione avvenuta correttamente"

    # Ritorniamo user_id
    id_user = r.get("id_utente:" + username)
    return id_user


# Creiamo una funzione per stampare la rubrica
def stampa_rubrica(id_user):
    # Otteniamo tutti i membri del set
    rubrica = r.smembers("rubrica:" + id_user)

    # Stampiamo la rubrica
    for username in rubrica:
        print(username)


def aggiungi_amico(username):
    if not r.exists("user:" + username):
        return "Inserisci un username esistente"

    # Se esiste, aggiungiamo l'amico alla rubrica
    r.zadd("rubrica:" + id_user, username)



r = connect()
registrazione_utente(inserimento())
