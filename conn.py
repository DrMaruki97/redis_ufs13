import redis 

def connect():
    r = redis.Redis(
        host='redis-10033.c328.europe-west3-1.gce.redns.redis-cloud.com',
        port=10033,
        password='kvgK4FP0P2HkKBsl2Vt5Odc2abp1e2mb',
        decode_response=True)
    return r
