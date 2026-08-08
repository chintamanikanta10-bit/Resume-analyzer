"""
chat.py

Handles user questions using RAG.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.summary_service import SummaryService

from config import LLM_MODEL
from core.auth import get_current_user
from database.models import User
from memory.memory import MemoryManager
from rag.prompt import PromptBuilder
from rag.retriever import RetrieverService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# --------------------------------------------------------
# Request Model
# --------------------------------------------------------

class ChatRequest(BaseModel):
    question: str


# --------------------------------------------------------
# Response Model
# --------------------------------------------------------

class ChatResponse(BaseModel):
    answer: str


# --------------------------------------------------------
# Initialize Services
# --------------------------------------------------------

retriever = RetrieverService()
prompt_builder = PromptBuilder()
memory = MemoryManager(window_size=10)
summary_service = SummaryService()


# --------------------------------------------------------
# Chat Endpoint
# --------------------------------------------------------

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):

    # ------------------------------------
    # Retrieve relevant document chunks
    # ------------------------------------

    documents = retriever.retrieve(
        request.question,
        user_id=current_user.id,
    )
    memory.add_user_message(request.question)

    # ------------------------------------
    # Build Prompt
    # ------------------------------------

    prompt = prompt_builder.build_prompt(
        documents,
        memory.get_chat_history(),
        memory.get_summary(),
    
        request.question
    )

    # ------------------------------------
    # Ask Gemini
    # ------------------------------------

    response = LLM_MODEL.generate_content(
        prompt
    )
    memory.add_ai_message(
        response.text
    )

    # ------------------------------------
    # Generate summary when history is full
    # ------------------------------------

    if memory.should_summarize():
        conversation = memory.get_full_conversation()
        summary = summary_service.generate_summary(
            memory.get_summary(),
            conversation
        )
        memory.update_summary(summary)
        memory.clear_chat_history()

    # ------------------------------------
    # Return Answer
    # ------------------------------------

    return ChatResponse(
        answer=response.text
    )