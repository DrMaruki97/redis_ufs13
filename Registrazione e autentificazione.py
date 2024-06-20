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
def autenticazione_utente(username, pwd):
    while True:
        inserimento()
        # Controlliamo l'esistenza dell'utente
        if r.exists(username):
            # Hashamo la pwd inserita
            check_pwd = hash_password(pwd)
            stored_pwd = r.get("user:" + username)

        if stored_pwd == check_pwd:
            print("Autenticazione avvenuta con successo")
            return True
        else:
            return False


# Creiamo una funzione per stampare la rubrica
def stampa_rubrica(username):
    # Otteniamo tutti i membri del set
    rubrica = r.smembers("rubrica:" + username)

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
