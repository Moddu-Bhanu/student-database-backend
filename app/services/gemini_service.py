import time

from google import genai
from google.genai.errors import ServerError

from app.core.config import settings


def generate_answer(question: str, student_context: str) -> str:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    prompt = f"""
You are a student database assistant.

Answer the user's question using only the student
database information provided below.

If the information is unavailable, say so.
Do not invent student records.
Do not reveal information that is not present
in the supplied context.

Student database information:
{student_context}

User question:
{question}
"""

    # Retry temporary Gemini server errors
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )

            if not response.text:
                return "I couldn't generate an answer. Please try again."

            return response.text

        except ServerError as e:
            if e.code == 503 and attempt == 0:
                time.sleep(3)
                continue

            if e.code == 503:
                return (
                    "Gemini is temporarily experiencing high demand. "
                    "Please try again in a few minutes."
                )

            raise

    return "I couldn't generate an answer. Please try again."