# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import login_with_google
from app.schemas.auth_schemas import GoogleLoginRequest

router = APIRouter()



@router.post("/google-login", status_code=status.HTTP_200_OK, summary="One Tap Google Login")
def google_login(payload: GoogleLoginRequest):
    return login_with_google(payload.id_token)
