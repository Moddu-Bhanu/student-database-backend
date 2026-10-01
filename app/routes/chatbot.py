import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.security import get_current_user
from app.models.user import User
from app.services.langgraph_service import run_chatbot
from app.services.vector_service import search_knowledge


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        # 1. Retrieve relevant knowledge from ChromaDB
        knowledge_results = search_knowledge(
            request.question,
            n_results=3,
        )

        # 2. Prepare the retrieved knowledge
        knowledge_context = "\n".join(
            result["text"]
            for result in knowledge_results
            if result.get("text")
        )

        if not knowledge_context:
            knowledge_context = "No relevant knowledge was found."

        # 3. Send the question and knowledge to LangGraph
        answer = run_chatbot(
            question=request.question,
            student_context=(
                "The user is authenticated. "
                "Use only the relevant knowledge provided below. "
                "Do not assume access to private student records.\n\n"
                f"Relevant knowledge:\n{knowledge_context}"
            ),
        )

        # 4. Return the chatbot response
        return {"answer": answer}

    except Exception:
        logger.exception(
            "Chatbot request failed for user ID %s",
            current_user.id,
        )

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question.",
        )