import redis 
import functions as f
import conn 

r = conn.connect()    # Uso la funzione di Davide per stabilire la connessione

salt = 'wasd'

comandi = {'LandingPage':['Login','Registration'],                          # Una lista di comandi, va data in argomento alle pagine
           'UserPage':['Set Dnd','Add contact','Chats'],                    # per stampare a schermo tutti i comandi che l'utente può
           'ChatPage':['Start new chat','Start timed chat','Active chats'], # chiamare
           'ActiveChat':[]
            }

intestazione = '='*10+'\nREDCHAT\n'+'='*10          # Semplice intestazione, va data in argomento alle pagine

page = 'LandingPage'

if r.exists('system:users'):
    sys_users = r.get('system:users')      # System:users è la chiave che contiene il numero di utenti registrati
else:                                      # verrà utilizzata per attribuire un ID ad ogni utente al momento della registrazione
    sys_user = 0
    r.set('system:user',0)

while True:                                      # Ciclo per mantenere il programma attivo, all'interno richiedo il comando
    f.Page(intestazione,comandi,page)          # all'utente, per poi dividere il flusso in base al comando
    action = f.action()

    if action in ('1','login'):
        user = input('Username >> ').lower()     # Dobbiamo trovare un modo più intelligente per gestire i vari comandi
        psw = input('Password >> ')
        
        if f.login(user,psw,salt,r):
            page = 'UserPage'
            break
        
        else:
            print('Username or Password not correct')
    
    elif action in ('2','registration'):
        user = input('Choose a Username >> ')
        sys_user = user.lower()
        
        while r.get(sys_user):
            print('Username not available')
            user = input('Choose a Username >> ')
            sys_user = user.lower()
        
        psw = input('Choose a Password >> ')
        
        if f.registration(user,psw,salt,r):
            print('Registration complete: you\'ll be directed to your page')
            page = 'UserPage'
            break
        
        else:
            print('ERROR: registration couldn\'t be completed')

while True:

    f.Page(intestazione,comandi,page)                  # Se abbiamo completato il login o la registrazione usciamo dal ciclo while ed 
    action = f.action()                                            # entriamo in un altro ciclo che rappresenta la pagina utente