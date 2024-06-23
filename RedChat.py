import redis 
import ui_functions as ui
import functions as f
import StreamMethods as sm
import threading as thr
import myfunctions as mf

r = mf.connect()    # Uso la funzione di Davide per stabilire la connessione

comandi = {'LandingPage':['Login','Registration','Exit'],                   # Una lista di comandi, va data in argomento alle pagine
           'UserPage':['Chat','Rubrica','DnD','Change Password','Logout'],  # per stampare a schermo tutti i comandi che l'utente può
           'ChatPage':['Start chat','Start timed chat','Home'],             # chiamare in una determinata pagina
           'RubricPage':['Aggiungi contatto','Rimuovi contatto','Home']
            }

intestazione = '='*11+'\n  REDCHAT  \n'+'='*11          # Semplice intestazione, va data in argomento alle pagine

page = 'LandingPage'


while True:                                             # Ciclo totale del programma, a seconda del valore di page esegue una
                                                        # "pagina" differente


    if page == 'LandingPage':

        while True:                                      # Ciclo per mantenere il programma attivo, all'interno richiedo il comando
            ui.page(intestazione,comandi,page)           # all'utente, per poi dividere il flusso in base al comando
            
            action = ui.action()

            if action in ('1','login'):
                
                user = input('Username >> ')
                psw = input('Password >> ')
                
                if mf.login(user,psw,r):
                    page = 'UserPage'
                    break
                
                else:
                    print('Username or Password not correct')
            
            elif action in ('2','registration'):
                
                print('Inserire Username e Password, lanciare un messagio vuoto per uscire dalla registrazione')

                while True:
                    
                    user = input('Choose a Username >> ')
                    disp = mf.check_disp(user,r)
                    if disp:
                        break
                    print('Username non disponibile')

                if not user:
                    break

                while True:
                    psw = input('Choose a Password >> ')
                    valid = mf.check_psw(psw)
                    if valid:
                        break
                    print('ERRORE: La password deve essere compresa tra 4 e 16 caratteri')
                
                if mf.registration(user,psw,r):
                    print('Registration complete: you\'ll be directed to your page')
                    page = 'UserPage'
                    break
                
                else:
                    print('ERROR: registration couldn\'t be completed')
            
            elif action in ('3','Close'):
                page = None
                break
            
            else:
                ui.wrg_cmd()

    if not page:
        break


    if page == 'UserPage':
        while True:

            ui.page(intestazione,comandi,page)            # Se abbiamo completato il login o la registrazione usciamo dal ciclo while ed 
                                                          # entriamo in un altro ciclo che rappresenta la pagina utente
            action = ui.action()

            if action in ('1','chat'):
                page = 'ChatPage'
                break

            elif action in ('2','rubrica'):
                page = 'RubricPage'
                break

            elif action in ('3','dnd'):
                dnd = f.check_dnd(user)
                if dnd:
                    print('DnD attualmente attivo')
                else:
                    print('DnD attualmente non attivo')
                
                while True:

                    choice = input('Modificare il proprio stato? [Y/N] ').lower()

                    if choice == 'y':
                        f.change_dnd(user)
                        break

                    elif choice == 'n':
                        break

                    else:
                        ui.wrg_cmd()

            elif action in ('4','change password'):

                while True: 
                    psw = input('Inserisci nuova password >> ')
                    
                    valid = mf.check_psw(psw)
                    if valid:
                        f.change_psw(user,psw,r)
                        break
                                       
                    else:
                        print('ERRORE: La password deve essere compresa tra 4 e 16 caratteri')
            
            elif action in ('5','logout'):
                page = 'LandingPage'
                break
            
            else:
                ui.wrg_cmd()




    if page == 'ChatPage':
        while True:
            o_user = False
            ui.page(intestazione,comandi,page)
            action = ui.action()

            if action in ('1','start chat'):

                lista = mf.get_friends(user)
                ui.view_list(lista)

                action = input('Con chi vuoi chattare?>> ')
                
                if action.isnumeric():
                    if int(action)< len(lista):
                        o_user = lista[int(action)]
                    else:
                        ui.wrg_cmd()
                
                else:
                    try:
                        lista.index(action)
                        o_user = action
                    except:
                        ui.wrg_cmd()
                
                if o_user:

                    print(f'CHAT CON {o_user}')
                    print('Invia un messaggio vuoto per uscire dalla chat')

                    values = r.hget(f'Rooms:{user}',o_user)

                    if values:
                    
                        values = values.split('::')
                        room = values[0]
                        chat = sm.get_chat(values[0],values[1])
                        new_chat = sm.get_new_msgs(values[0],values[1])
                        ui.msgs(user,chat)
                        if new_chat:
                            print('---- Nuovi Messaggi ----\n')
                            ui.msgs(user,new_chat)

                    else:
                        
                        messaggio = ui.speak(user)
                        if messaggio:
                            room = sm.send_message(user,o_user,messaggio)
                        else:
                            break

                    event = thr.Event()
                    event.set()

                    t1 = thr.Thread(target=sm.eavesdropping,args=(room,user,o_user,event))
                    t1.start()

                    while True:

                        messaggio = ui.speak(user)

                        if messaggio:                            
                            sm.send_message(user,o_user,messaggio)
                        
                        else:
                            event.clear()
                            t1.join()
                            break                        


            elif action in ('2','start timed chat'):

                lista = f.GetFriends(user)
                ui.chats(lista)

                action = input('Con chi vuoi chattare?>> ')
                
                if action.isnumeric():
                    if int(action)< len(lista):
                        o_user = lista[int(action)]
                    else:
                        ui.wrg_cmd()
                
                else:
                    try:
                        lista.index(action)
                        o_user = action
                    except:
                        ui.wrg_cmd()
                
                if o_user:

                    print(f'CHAT A TEMPO CON {o_user}')
                    print('Invia un messaggio vuoto per uscire dalla chat')

                    values = r.hget(f'Timed:Rooms:{user}',o_user)

                    if values:
                    
                        values = values.split('::')
                        room = values[0]
                        chat = sm.get_chat(values[0],values[1])
                        new_chat = sm.get_new_msgs(values[0],values[1])
                        ui.msgs(user,chat)
                        if new_chat:
                            print('---- Nuovi Messaggi ----\n')
                            ui.msgs(user,new_chat)

                    else:
                        
                        messaggio = ui.speak(user)
                        if messaggio:
                            room = sm.send_timed_message(user,o_user,messaggio)
                        else:
                            break

                    event = thr.Event()
                    event.set()

                    t1 = thr.Thread(target=sm.eavesdropping,args=(room,user,o_user,event))
                    t1.start()

                    while True:

                        messaggio = ui.speak(user)

                        if messaggio:                            
                            sm.send_message(user,o_user,messaggio)
                            sm.set_timer(room)
                        
                        else:
                            event.clear()
                            t1.join()
                            break
            
            elif action in ('3','home'):
                page = 'UserPage'
                break

            else:
                ui.wrg_cmd()




    if page == 'RubricPage':
        while True:
            ui.page(intestazione,comandi,page)
            action = ui.action()
            
            if action in ('1','aggiungi contatto'):
                print('Ricerca username,anche parziale')

                ricerca = ui.action()
                utenti = mf.user_serch(ricerca)
                ui.view_list(utenti)

                selezione = ui.action()

                if action.isnumeric():
                    if int(action)< len(lista):
                        friend = lista[int(action)]
                    else:
                        ui.wrg_cmd()
                
                else:
                    try:
                        lista.index(action)
                        friend = action
                    except:
                        ui.wrg_cmd()
                
                if friend:
                    
                    mf.add_friend(friend)


            elif action in ('2','rimuovi contatto'):
                print('n\'altra volta')
            elif action in ('3','home'):
                page = 'UserPage'
                break
            else:
                ui.wrg_cmd()

print('Grazie e arrivederci')