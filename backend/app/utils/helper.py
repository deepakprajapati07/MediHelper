# app/utils/helper.py

import re

def format_dialogue(conversation: list[dict]) -> str:
    """
    Converts list of chat messages into a formatted string for LLM input.
    """
    formatted_dialogue = "Chat History:\n\n"
    for message in conversation:
        user_input = message.get("user")
        assistant_response = message.get("assistant")

        if user_input:
            formatted_dialogue += f"Human: {user_input}\n"
        if assistant_response:
            formatted_dialogue += f"AI: {assistant_response}\n"

        formatted_dialogue += "\n"

    return formatted_dialogue.strip()

def format_context(context_str):
    return f"More Context:\n\n{context_str}"

