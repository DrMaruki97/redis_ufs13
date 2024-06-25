from chat import chat_interface, history_chat, dnd_on
from functions import change_psw, open_group, create_group
from functions import login, start_form, find_user, id_maker, connect, sign_up, add_friends, set_dnd_on, set_dnd_off


if __name__ == "__main__":
    r = connect()
    print("[1] Login or [2] Sign Up")
    if int(input("1 or 2? ")) == 1:
        usr, pwd = start_form()
        lista = login(usr, pwd)
    else:
        usr, pwd = start_form()
        lista = sign_up(usr, pwd)
    if lista:
        user = usr
        id_user = r.get(f"id_user:{user}")
    else:
        print("Something went wrong, try again!")
        exit()
    print()
    print(f"Welcome, {user}!")

    while True:
        print()
        print("---MAIN MENU---")
        print(f"[1]|Chats [2]|Add friend [3]|Do-not-Disturb [4]|Change password [5]|Exit")
        print()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            while True:
                print()
                print(f" [1]|Personal Chats [2]|Group Chats")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    contatti = r.smembers(f"contacts:{user}")
                    contatti = list(contatti)
                    if contatti:
                        for a, b in enumerate(contatti):
                            print(f"{a}: {b}")
                        choice = int(input("Choose the user: "))
                        friend = contatti[choice]
                        if not dnd_on(friend):
                            id_chat = id_maker(id_user, friend)
                            print(id_chat)  # serve a noi, poi lo eliminiamo
                            channel = f"channel:{id_chat}"
                            history_chat(id_chat)
                            chat_interface(user, channel, id_user)
                            print(f"You opened the chat with {friend}!")
                    else:
                        print("You do not have any friends, add one first!")
                elif choice == 2:
                    print(f" [1]|Apri gruppi [2]|Crea Gruppi")
                    choice = int(input("Enter your choice: "))
                    if choice == 1:
                        id_chat = open_group()
                    else:
                        nome_chat = input("Scegli un nome per la chat: ")
                        id_chat = create_group(nome_chat)
                    group_chat = f"room:{id_chat}"
                    print(id_chat)
                    history_chat(id_chat)
                    chat_interface(user, group_chat, id_user)


        elif choice == 2:
            key = input("Enter the username of the user: ")
            risultati = find_user(key)
            if risultati:
                for a, b in enumerate(risultati):
                    print(f"{a}: {b}")
                choice = int(input("Choose the user: "))
                if add_friends(user, risultati[choice]):
                    print(f"You and {risultati[choice]} are now friends!")
            else:
                print("Sorry, no friend found with this username!")

        elif choice == 3:
            if r.getbit(f"dndmap", int(id_user)) == "0":
                answer = input("Do you wanna activate Do-Not-Disturb mode? (Y/n) ")
                if answer == "Y" or answer == "y":
                    c = set_dnd_on(id_user)
                    if c:
                        print("Do-Not-Disturb mode activated")
                else:
                    pass
            else:
                answer = input("Do you wanna Deactivate Do-Not-Disturb mode? (Y/n) ")
                if answer == "Y" or answer == "y":
                    c = set_dnd_off(id_user)
                    if c:
                        print("Do-Not-Disturb mode deactivated")
                else:
                    pass

        elif choice == 4:
            new_password = input("Write a new password: ")
            c = change_psw(user, new_password)
            if c:
                print("Password changed successfully")

        elif choice == 5:
            print(f"Goodbye {user}, see you space cowboy...")
            break

        else:
            pass
