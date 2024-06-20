import redis 
import ui_functions as ui
import conn 

r = conn.connect()    # Uso la funzione di Davide per stabilire la connessione

comandi = {'LandingPage':['Login','Registration'],                          # Una lista di comandi, va data in argomento alle pagine
           'UserPage':['Chat','Rubrica','DnD','Change Password'],           # per stampare a schermo tutti i comandi che l'utente può
           'ChatPage':['Active chats','Start new chat','Start timed chat'], # chiamare
           'ActiveChat':[],
           'RubricPage':['Vedi Rubrica','Aggiungi contatto','Rimuovi contatto']
            }

intestazione = '='*10+'\nREDCHAT\n'+'='*10          # Semplice intestazione, va data in argomento alle pagine

page = 'LandingPage'

if r.exists('system:users'):
    sys_users = r.get('system:users')      # System:users è la chiave che contiene il numero di utenti registrati
else:                                      # verrà utilizzata per attribuire un ID ad ogni utente al momento della registrazione
    sys_user = 0
    r.set('system:user',0)

while True:                                      # Ciclo per mantenere il programma attivo, all'interno richiedo il comando
    action = ui.Page(intestazione,comandi,page)   # all'utente, per poi dividere il flusso in base al comando
    

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
    else:
        ui.wrg_cmd()



while True:

    action = ui.Page(intestazione,comandi,page)                  # Se abbiamo completato il login o la registrazione usciamo dal ciclo while ed 
                                                                 # entriamo in un altro ciclo che rappresenta la pagina utente

    if action in ('1','chat'):
        page = 'ChatPage'
        break

    elif action in ('2','rubrica'):
        page = 'RubricPage'
        break

    elif action in ('3','dnd'):
        dnd = r.get(f'DnD:{user}')
        if dnd:
            print('DnD attualmente attivo')
        else:
            print('DnD attualmente non attivo')
        
        choice = 'k'
        while choice not in ('y','n'):

            choice = input('Modificare il proprio stato? [Y/N] ').lower()

            if choice == 'y':
                r.set(f'DnD:{user}', not dnd)
                break

            elif choice == 'n':
                break

            else:
                ui.wrg_cmd()


    elif action in ('4','change password'):

        while True: 
            psw = input('Inserisci nuova password >> ')
            
            if len(psw) < 4 or len(psw) > 16:
                print('Password non valida, deve essere compresa tra 5 e 16 caratteri')
            
            else:
                r.set()
    else:
        ui.wrg_cmd()



if page == 'ChatPage':
    while True:
        action = page(intestazione,comandi,page)

        if action in ('1','active chats'):
            # Get_active_Chats
        elif action in ('2','start new chat'):


        elif action in ('3','start timed chat'):

        else:
            ui.wrg_cmd()




if page == 'RubricPage':
    while True:
        action = page(intestazione,comandi,page)
        
        if action in ('1','vedi rubrica'):
        elif action in ('2','aggiungi contatto'):
        elif action in ('3','rimuovi contatto'):
        else:
            ui.wrg_cmd()