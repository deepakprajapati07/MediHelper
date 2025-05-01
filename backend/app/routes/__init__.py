# app/routes/__init__.py

from fastapi import APIRouter, status, HTTPException
from . import auth, chatbot

api_router = APIRouter()

# Include all the routers here
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
    responses={
        500: {"description": "Internal Server Error"},
    }
)

api_router.include_router(
    chatbot.router,
    prefix="/chatbot",
    tags=["ChatBot"],
    responses={
        500: {"description": "Internal Server Error"},
    }
)

__all__ = ["api_router"]