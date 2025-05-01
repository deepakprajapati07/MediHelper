# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.mongo import connect_to_mongo, close_mongo_connection
from app.firebase_config import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup/shutdown for DBs and models."""
    
    # MongoDB Connection
    connect_to_mongo()
    yield

    # Clean up resources
    close_mongo_connection()
    print("✅ Resources cleaned up.")
