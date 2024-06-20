# c'è bisogno di una mano per l'hash della pw eee spero di aver capito bene e di non aver fatto grandi scempiate ma è
# stato più difficile di quanto mi aspettassi
import bcrypt # libreria per hashing delle pwd
import redis
username = input("Inserisci un nome utente: ")
pwd = input("Inserisci un password utente: ")

# Creiamo una funzione di registrazione utente

def registrazione_utente(username, pwd,r):

    # Controlliamo l'unicità del nome utente
    if r.exists(username):
        return "Nome utente già eistente"

    # Controlliamo che la password abbia lunghezza compresa tra 4 e 16 caratteri
    if len(pwd) < 4 or len(pwd) > 16:
        return "Inserisci una password valida"

    # Facciamo in modo di non salvare in bianco la password
    pwd_hash = hash_password(pwd)

    # Creiamo istanza redis per l'utente
    r.set("user:" + username, pwd_hash)

    # Creiamo un id utente
    id_user = r.incr("id_utente")

    # Creiamo istanza redis per id utente
    r.set("id_utente:" + username, id_user)

    # Creiamo istanza rubrica
    r.zadd('rubrica:' + id_user, {'membro1': 1.0, 'membro2': 2.0})


# Creiamo una funzione di identificazione

def autentificazione_utente(username, pwd):

    # Controlliamo l'esistenza dell'utente
    if not r.exists(username):
        return "Utente non esistente"

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
    r.zadd("rubrica:" + id_user , username)



