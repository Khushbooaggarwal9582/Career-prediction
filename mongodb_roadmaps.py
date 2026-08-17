import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "career_compass")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "roadmaps")


def check_mongodb():
    # Ping MongoDB once at startup with a very short timeout (400ms)
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=400)
        client.admin.command("ping")
        return True
    except Exception:
        return False


HAS_MONGO = check_mongodb()


def get_collection():
    if not HAS_MONGO:
        raise PyMongoError("MongoDB is offline")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
    return client[MONGO_DB][MONGO_COLLECTION]


def get_roadmap(career):
    if not HAS_MONGO:
        return None
    try:
        collection = get_collection()
        return collection.find_one(
            {"career": career},
            {"_id": 0, "career": 1, "domain": 1, "steps": 1},
        )
    except Exception:
        return None
