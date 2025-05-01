# app/firebase_config.py

import firebase_admin
from firebase_admin import credentials
from app.config import settings

# Prepare Firebase credentials
firebase_credentials = {
    "type": "service_account",
    "project_id": settings.firebase_project_id,
    "private_key_id": settings.private_key_id,
    "private_key": settings.firebase_private_key.replace("\\n", "\n"),
    "client_email": settings.firebase_client_email,
    "client_id": settings.client_id,
    "auth_uri": settings.auth_uri,
    "token_uri": settings.token_uri,
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.firebase_client_email.replace('@', '%40')}"
}

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
