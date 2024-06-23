from chat import chat_interface, history_chat, dnd_on
from functions import login, start_form, select_user, hash_pwd2, connect, sign_up, add_friends, set_dnd_on, set_dnd_off
from functions import change_psw


if __name__ == "__main__":
    r = connect()
    print("[1] Login or [2] Sign Up")
    if int(input("1 or 2? ")) == 1:
        usr, pwd = start_form()
        lista = login(usr, pwd)
    else:
        usr, pwd = start_form()
        lista = sign_up(usr, pwd)
    user = lista[2]
    id_user = lista[1]
    print()
    print(f"Welcome back, {user}!")

    while True:
        print()
        print("---MAIN MENU---")
        print(f"[1]|Chats [2]|Add friend [3]|Do-not-Disturb [4]|Change password [5]|Exit")
        print()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            friend = "alexa" #FUNZIONE DA FINIRE "placeholder name"
            print(f"You opened the chat with {friend}!")
            if not dnd_on(friend):
                id_chat = hash_pwd2(f"{user}:{friend}")
                print(id_chat) #serve a noi, poi lo eliminiamo
                channel = f"channel:{id_chat}"
                history_chat(id_chat)
                chat_interface(user, channel)

        elif choice == 2:
            new_friend = select_user() #Funzione da finire "placeholder"
            add_friends(user, new_friend)

        elif choice == 3:
            if not dnd_on(user):
                answer = input("Do you wanna activate Do-Not-Disturb mode? (Y/n) ")
                if answer == "Y" or "y":
                    c = set_dnd_on(user, id_user)
                    if c:
                        print("Do-Not-Disturb mode activated")
                else:
                    pass
            else:
                answer = input("Do you wanna deactivate Do-Not-Disturb mode? (Y/n) ")
                if answer == "Y" or "y":
                    c = set_dnd_off(user, id_user)
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









