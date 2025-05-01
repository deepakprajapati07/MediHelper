# app/services/chatbot_utils.py

from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from app.config import settings
from app.utils.helper import format_context
from app.utils.constants import PROMPT_TEMPLATE
import os

os.environ['GOOGLE_API_KEY'] = settings.gemini_api_key

class ChatModelService:
    def __init__(self):
        self.prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    def get_model(self, model_name: str) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=settings.llm_temperature
        )

    def generate_response(self, model_name: str, context: str, user_input: str):
        llm = self.get_model(model_name)
        chain: RunnableSequence = self.prompt | llm
        return chain.invoke({"context": context, "question": user_input})


class ChatContextService:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model=settings.embedding_model)
        self.vector_db = Chroma(
            persist_directory=settings.vector_db_path,
            embedding_function=self.embedding_model
        )

    def retrieve(self, user_input: str) -> str:
        retriever = self.vector_db.as_retriever(search_kwargs={"k": settings.vector_db_k})
        context_docs = retriever.invoke(user_input)
        combined_context = "\n\n".join(doc.page_content for doc in context_docs)
        return format_context(combined_context)

