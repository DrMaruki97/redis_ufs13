import redis 
import ui_functions as ui
import functions as f
import chat as ch
import threading as thr


if __name__ == '__main__':

    r = f.connect()    # Uso la funzione di Davide per stabilire la connessione

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
                    
                    user,psw = f.start_form()
                    
                    if f.login(user,psw):
                        page = 'UserPage'
                        break
                    
                    else:
                        print('Username o Password non corretti')
                
                elif action in ('2','registration'):
                    
                    print('Inserire Username e Password, premere <enter> per uscire per uscire dalla registrazione')
                    print('RESTRIZIONI:\nUsername => max 20 caratteri\nPassword => compresa tra 4 e 16 caratteri')

                    while True:
                        
                        user = input('Scegli uno Username >> ')
                        if f.check_disp(user):
                            break
                        print('Username non disponibile')

                    if not user:
                        break

                    while True:
                        psw = input('Scegli una Password >> ')
                        if f.check_psw(psw):
                            break
                        print('ERRORE: Password non valida')
                    
                    if f.sign_up(user,psw):
                        print('Registrazione completata')
                        page = 'UserPage'
                        break
                    
                    else:
                        print('ERRORE: Non abbiamo potuto completare al tua registrazione')
                
                elif action in ('3','Close'):
                    page = None
                    break
                
                else:
                    ui.wrg_cmd()

        if not page:
            break


        if page == 'UserPage':

            user_id = r.get(f'id_user:{user}')

            while True:
                
                print(f'Benvenuto, {user}\n\n')
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
                    dnd = f.check_dnd(user_id)
                    if dnd:
                        print('DnD attualmente attivo')
                    else:
                        print('DnD attualmente non attivo')
                    
                    while True:

                        choice = input('Modificare il proprio stato? [Y/N] ').lower()

                        if choice == 'y':
                            f.change_dnd(user,dnd)
                            break

                        elif choice == 'n':
                            break

                        else:
                            ui.wrg_cmd()

                elif action in ('4','change password'):

                    while True: 
                        psw = input('Inserisci nuova password >> ')
                        
                        if f.check_psw(psw):
                            f.change_psw(user,psw)
                            break
                                        
                        else:
                            print('ERRORE: Password non valida')
                
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

                    contatti = f.get_friends(user)

                    if contatti:
                        ui.view_list(lista)

                        action = input('Con chi vuoi chattare?>> ')
                        
                        if action.isnumeric():
                            if int(action) <= len(lista):
                                o_user = lista[int(action)-1]
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
                            print('premi <enter> per uscire dalla chat')

                            id_chat = f.id_maker(user_id, o_user)
                            channel = f'channel:{id_chat}'
                            ch.history_chat(id_chat)

                            event = thr.Event()
                            event.set()

                            t1 = thr.Thread(target=sm.eavesdropping,args=(room,user,o_user,event,r))
                            t1.start()

                            while True:

                                messaggio = ui.speak(user)

                                if messaggio:                            
                                    sm.send_message(user,o_user,r,messaggio)
                                
                                else:
                                    event.clear()
                                    t1.join()
                                    break 
                                              
                    else:
                        print('Non hai ancora alcun contatto, aggiungi i tuoi amici!')

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
                    utenti = mf.user_serch(ricerca,r)
                    ui.view_list(utenti)

                    selezione = ui.action()

                    if action.isnumeric():
                        if int(action)<= len(utenti):
                            friend = utenti[int(action)-1]
                        else:
                            ui.wrg_cmd()
                    
                    else:
                        try:
                            utenti.index(action)
                            friend = action
                        except:
                            ui.wrg_cmd()
                    
                    if friend:
                        
                        mf.add_friend(user,friend,r)


                elif action in ('2','rimuovi contatto'):
                    print('n\'altra volta')
                elif action in ('3','home'):
                    page = 'UserPage'
                    break
                else:
                    ui.wrg_cmd()

    print('Grazie e arrivederci')