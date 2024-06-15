# Ho creato un account redis dove è presente un server condiviso. Queste sono le credenziali dell'account:
# 'chadgippidy@gmail.com'
# 'QuackQuack123!'

# L'indirizzo del server è 'redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com:16230'
# La password per accedere al server è: 'y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL'
# Lo username è 'default'
# Inserire le credenziali sul git non è per nulla sicuro, ma è ok fino a quando la repo è privata e stiamo sperimentando


import redis 

r = redis.Redis(
  host='redis-16230.c328.europe-west3-1.gce.redns.redis-cloud.com',
  port=16230,
  password='y6ORUWqEjBvQZU3ICfuV8dgU8glOYFwL')
# Per collegarsi al server Redis basta creare un oggetto Redis dove si specificano host, porta e password. Trovate tutte queste informazioni su Redis Cloud.


r.set("Alexa","Suona Despacito")
#semplice set

print(r.get("Alexa"))
#semplice get