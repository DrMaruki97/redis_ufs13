import redis 
import functions as f

r = redis.Redis(
  host='redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com',
  port=16230,
  password='y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL',
  decode_responses=True)

salt = 'wasd'

comandi = {'LandingPage':['Login','Registration'],
           'UserPage':['Set Dnd','Add contact','Chats'],
           'ChatPage':['Start new chat','Start timed chat','Active chats']
            }

intestazione = '='*10+'\nREDCHAT\n'+'='*10


while True:
    f.LandingPage(intestazione,comandi)
    action = input('>> ').lower()
    if action in ('1','login'):
        user = input('Username >> ').lower()
        psw = input('Password >> ')
        if f.login(user,psw,salt,r):
            break
        else:
            print('Username or Password not correct')
    elif action in ('2','registration'):
        user = input('Choose a Username >> ')
        sys_user = user.lower()
        while r.get(sys_user):
            print('Username not available')
            user = input('Choose a Username >> ').lower()
        psw = input('Choose a Password >> ')
        if f.registration(user,psw,salt,r):
            print('Registration complete: you\'ll be directed to your page')
            break
        else:
            print('ERROR: registration couldn\'t be completed')

f.UserPage(intestazione,comandi)


