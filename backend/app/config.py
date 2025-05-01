# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    
    mongo_uri: str
    mongo_db_name: str
    mongo_db_username: str
    mongo_db_password: Optional[str] = None
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    private_key_id: str
    firebase_client_email: str
    firebase_project_id: str
    client_id: str
    token_uri: str
    auth_uri: str
    firebase_private_key: str
    
    langchain_api_key: str
    gemini_api_key: str
    llm_model_1: str
    llm_model_2: str
    embedding_model: str
    vector_db_path: str
    vector_db_k: int
    llm_temperature: int
    memory_limit: int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="allow"
    )
    
    def safe_dict(self) -> dict:
        """
        Returns a copy of settings with sensitive values masked.
        """
        sensitive_keys = {
            "mongo_db_username",
            "mongo_db_password",
            "secret_key",
            "algorithm",
            "private_key_id",
            "firebase_private_key",
            "firebase_client_email",
            "firebase_project_id",
            "client_id",
            "token_uri",
            "auth_uri",
            "langchain_api_key",
            "gemini_api_key",
        }

        data = self.model_dump()
        for key in sensitive_keys:
            if key in data and data[key] is not None:
                data[key] = "******"
        return data

# Usage
settings = Settings()

# print(settings.safe_dict())