
### Connettersi a Redis
import redis

# Connessione al server Redis in esecuzione sulla porta 6379 sul localhost
r = redis.Redis(host='localhost', port=6379, db=0)


### 1. Comandi per le Stringhe

# Impostare un valore
r.set('chiave', 'valore')

# Ottenere un valore
valore = r.get('chiave')
print(valore)  # Output: b'valore'

# Impostare più valori
r.mset({'chiave1': 'valore1', 'chiave2': 'valore2'})

# Ottenere più valori
valori = r.mget('chiave1', 'chiave2')
print(valori)  # Output: [b'valore1', b'valore2']

# Cancellare chiavi
r.delete('chiave1', 'chiave2')


### 2. Comandi per i Numeri

# Impostare un valore numerico
r.set('numero', 10)

# Incrementare di 1
r.incr('numero')

# Decrementare di 1
r.decr('numero')

# Incrementare di un valore specificato
r.incrby('numero', 5)

# Incrementare di un valore float specificato
r.incrbyfloat('numero', 2.5)


### 3. Comandi per le Bitmap

# Impostare un bit
r.setbit('bitmap', 10, 1)

# Ottenere un bit
bit = r.getbit('bitmap', 10)
print(bit)  # Output: 1

# Contare i bit settati a 1
bitcount = r.bitcount('bitmap')
print(bitcount)  # Output: 1

# Operazioni bit a bit
r.set('bitmap1', 'foo')
r.set('bitmap2', 'bar')
r.bitop('and', 'bitmap_dest', 'bitmap1', 'bitmap2')


### 4. Comandi per le Liste

# Inserire valori in coda
r.rpush('lista', 'valore1', 'valore2')

# Inserire valori in testa
r.lpush('lista', 'valore3')

# Ottenere la lunghezza della lista
lunghezza = r.llen('lista')
print(lunghezza)  # Output: 3

# Ottenere un elemento per indice
elemento = r.lindex('lista', 0)
print(elemento)  # Output: b'valore3'

# Rimuovere e ottenere il primo elemento
primo_elemento = r.lpop('lista')
print(primo_elemento)  # Output: b'valore3'

# Rimuovere e ottenere l'ultimo elemento
ultimo_elemento = r.rpop('lista')
print(ultimo_elemento)  # Output: b'valore2'

# Ottenere una gamma di elementi
elementi = r.lrange('lista', 0, -1)
print(elementi)  # Output: [b'valore1']


### 5. Comandi per gli Hash

# Impostare un campo in un hash
r.hset('hash', 'campo1', 'valore1')

# Impostare più campi in un hash
r.hmset('hash', {'campo2': 'valore2', 'campo3': 'valore3'})

# Ottenere il valore di un campo
valore = r.hget('hash', 'campo1')
print(valore)  # Output: b'valore1'

# Ottenere tutti i campi e valori
hash_completo = r.hgetall('hash')
print(hash_completo)  # Output: {b'campo1': b'valore1', b'campo2': b'valore2', b'campo3': b'valore3'}

# Cancellare un campo
r.hdel('hash', 'campo1')

# Incrementare un campo numerico
r.hincrby('hash', 'campo2', 5)


### 6. Comandi per i Set

# Aggiungere valori a un set
r.sadd('set', 'valore1', 'valore2')

# Controllare se un valore è membro del set
membro = r.sismember('set', 'valore1')
print(membro)  # Output: True

# Ottenere tutti i membri del set
membri = r.smembers('set')
print(membri)  # Output: {b'valore1', b'valore2'}

# Rimuovere valori dal set
r.srem('set', 'valore1')

# Intersezione di set
intersezione = r.sinter('set1', 'set2')
print(intersezione)

# Differenza di set
differenza = r.sdiff('set1', 'set2')
print(differenza)

# Unione di set
unione = r.sunion('set1', 'set2')
print(unione)

# Ottenere la cardinalità del set
cardinalità = r.scard('set')
print(cardinalità)


### 7. Comandi per gli Sorted Set

# Aggiungere membri a uno sorted set con uno score
r.zadd('sorted_set', {'membro1': 1.0, 'membro2': 2.0})

# Ottenere una gamma di membri
membri = r.zrange('sorted_set', 0, -1, withscores=True)
print(membri)  # Output: [(b'membro1', 1.0), (b'membro2', 2.0)]

# Rimuovere membri
r.zrem('sorted_set', 'membro1')


### 8. Altre Operazioni

# Impostare una scadenza per una chiave
r.expire('chiave', 10)

# Ottenere il tempo di vita rimanente di una chiave
ttl = r.ttl('chiave')
print(ttl)
