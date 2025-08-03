import uuid
from app.database import *

def get_shard_collection(short_id: str):
    prefix = short_id[0].lower()
    return shards.get(prefix, shards['default'])

def generate_shorten_url() -> str:
    while True:
        short_id = uuid.uuid4().hex[:6]
        shard = get_shard_collection(short_id)
        existing = shard.find_one({"short_id": short_id})
        if not existing:
            return short_id
        
def save_url(long_url:str)->str:
    short_id = generate_shorten_url()
    print("short id", short_id)

    shard = get_shard_collection(short_id)
    shard.insert_one({"short_id": short_id, "long_url": str(long_url)})

    print("HELLO")
    return short_id

def retrieve_function(short_id: str) -> str:
    cache_url = cache.get(short_id)
    if cache_url:
        print("Success getting a url from cache")
        cache.incr(f"analytics:{short_id}")
        return cache_url 

    print("missing getting cache url")
    shard = get_shard_collection(short_id)
    doc = shard.find_one({"short_id": short_id})
    if doc:
        long_url = doc["long_url"]
        cache.set(short_id, long_url, ex=3600)
        cache.incr(f"analytics:{short_id}")
        return long_url
    return None