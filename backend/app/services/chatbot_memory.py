# app/services/chatbot_memory.py

from langchain.memory import ConversationBufferMemory
from pydantic import Field
from typing import Dict

class LimitedConversationBufferMemory(ConversationBufferMemory):
    max_limit: int = Field(default=20, alias="max_limit")

    def __init__(self, memory_key="history", input_key="question", output_key="response", max_limit=20):
        super().__init__(memory_key=memory_key, input_key=input_key, output_key=output_key)
        self.max_limit = max_limit

    def is_memory_full(self) -> bool:
        return len(self.chat_memory.messages) >= self.max_limit

    def delete_oldest_item(self):
        if self.chat_memory.messages:
            self.chat_memory.messages.pop(0)

    def save_context_with_limit_check(self, inputs: Dict[str, str], outputs: Dict[str, str]):
        if self.is_memory_full():
            self.delete_oldest_item()
        super().save_context(inputs, outputs)


