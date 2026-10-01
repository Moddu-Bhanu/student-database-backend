from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, student_data: StudentCreate):
    existing_student = (
        db.query(Student)
        .filter(Student.email == student_data.email)
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists"
        )

    student = Student(**student_data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):
    student = get_student(db, student_id)
    update_data = student_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = (
            db.query(Student)
            .filter(
                Student.email == update_data["email"],
                Student.id != student_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists"
            )

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}