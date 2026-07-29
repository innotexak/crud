import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGO_URL = os.environ["MONGODB_URL"]

client = AsyncMongoClient(MONGO_URL)
db = client["fast-api"]

def get_collection(collection_name: str):
    return db.get_collection(collection_name)

post_collection = get_collection("posts")