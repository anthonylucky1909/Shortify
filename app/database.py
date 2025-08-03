from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient
import redis

# Load variables from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# MongoDB connection
client = MongoClient(MONGO_URI)
database = client.url_shortener
collection = database.url
shards = {
    'a': database['url_a'],
    'b': database['url_b'],
    'c': database['url_c'],
    'd': database['url_d'],
    'e': database['url_e'],
    'f': database['url_f'],
    'default': database['url_default']
}

# Redis connection
cache = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)
