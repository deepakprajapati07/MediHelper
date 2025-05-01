# app/schemas/auth_schemas.py

from pydantic import BaseModel

class GoogleLoginRequest(BaseModel):
    id_token: str
    
