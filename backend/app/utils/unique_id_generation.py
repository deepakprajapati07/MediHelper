# app/utils/unique_id_generation.py

from datetime import datetime

def generate_unique_user_id() -> str:
    prefix = "USER"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_id = f"{prefix}_{timestamp}"
    return unique_id


def generate_unique_chat_session_id() -> str:
    prefix = "CHAT"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_id = f"{prefix}_{timestamp}"
    return unique_id

