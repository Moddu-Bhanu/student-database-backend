from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.services.gemini_service import generate_answer


class ChatState(TypedDict):
    question: str
    student_context: str
    answer: str


def generate_response(state: ChatState) -> dict:
    answer = generate_answer(
        question=state["question"],
        student_context=state["student_context"]
    )

    return {"answer": answer}


def build_chatbot():
    workflow = StateGraph(ChatState)

    workflow.add_node("generate_response", generate_response)

    workflow.add_edge(START, "generate_response")
    workflow.add_edge("generate_response", END)

    return workflow.compile()


chatbot = build_chatbot()


def run_chatbot(question: str, student_context: str) -> str:
    result = chatbot.invoke({
        "question": question,
        "student_context": student_context,
        "answer": ""
    })

    return result["answer"]