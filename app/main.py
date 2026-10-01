from fastapi import FastAPI

from app.routes.chatbot import router as chatbot_router
from app.core.database import Base, engine
from app.models.student import Student
from app.models.user import User
from app.routes.students import router as students_router
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Database Application System",
    description="Backend API for managing student information",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Student Database Backend is running"
    }


app.include_router(students_router)
app.include_router(chatbot_router)
app.include_router(auth_router)