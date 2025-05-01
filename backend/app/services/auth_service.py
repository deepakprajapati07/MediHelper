# app/services/auth_service.py

from firebase_admin import auth
from fastapi import HTTPException, status
from app.database.mongo import users_collection
from datetime import datetime, timezone
from app.utils.unique_id_generation import generate_unique_user_id
from app.utils.oauth import create_access_token

def verify_firebase_token(id_token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )

def get_or_create_user(decoded_token: dict) -> dict:
    uid = decoded_token["uid"]
    email = decoded_token.get("email")
    name = decoded_token.get("name", "")

    user = users_collection.find_one({"uid": uid})
    if user:
        return user
    
    new_user = {
        "user_id": generate_unique_user_id(),
        "uid": uid,
        "email": email,
        "name": name,
        "created_at": datetime.now(timezone.utc)
    }
    users_collection.insert_one(new_user)
    return new_user

def login_with_google(id_token: str) -> dict:
    decoded_token = verify_firebase_token(id_token)
    user = get_or_create_user(decoded_token)
    
    access_token = create_access_token(
        data={"sub": user["user_id"], "uid": user["uid"], "email": user["email"]}
    )
    
    print(f"\nJWT Access Token: {access_token}\n")

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "uid": user["uid"],
            "email": user["email"],
            "name": user["name"],
        }
    }

