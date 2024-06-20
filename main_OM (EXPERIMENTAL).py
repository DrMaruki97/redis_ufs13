# Uso un altro server per sperimentare con Redis OM e Streamlit. Può essere utile per capire come funziona Redis velocemente
#redis-10033.c328.europe-west3-1.gce.redns.redis-cloud.com:10033
#kvgK4FP0P2HkKBsl2Vt5Odc2abp1e2mb

# Redis OM connection to remote server https://github.com/redis/redis-om-python/blob/main/docs/connections.md

import redis 
from redis_om import HashModel
import datetime
from typing import Optional

r = redis.Redis(
        host='redis-10033.c328.europe-west3-1.gce.redns.redis-cloud.com',
        port=10033,
        password='kvgK4FP0P2HkKBsl2Vt5Odc2abp1e2mb')


class User(HashModel):
    first_name: str
    last_name: str
    email: str
    join_date: datetime.date
    age: int
    bio: Optional[str] = 'Quack Quack motherfucker.'

    class Meta:
      database = r 


andrew = User(
    first_name="Andrew",
    last_name="Brookins",
    email="andrew.brookins@example.com",
    join_date=datetime.date.today(),
    age=38
)

print(andrew.pk)
andrew.save()