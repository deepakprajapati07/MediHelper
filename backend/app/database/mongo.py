# app/database/mongo.py

import logging
from pymongo import MongoClient
from pymongo.database import Database
from app.config import settings

logger = logging.getLogger(__name__)

client = MongoClient(settings.mongo_uri)
mongo_db: Database = client[settings.mongo_db_name]

users_collection = mongo_db["users"]
chatbot_session_collection = mongo_db["chatbot_session"]
chatbot_history_collection = mongo_db["chatbot_history"]

def connect_to_mongo():
    try:
        mongo_db.command("ping")
        logger.info("✅ Connected to MongoDB")
    except Exception as e:
        logger.error(f"❌ MongoDB connection error: {e}")

def close_mongo_connection():
    client.close()
    logger.info("MongoDB connection closed")
