from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=100)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    course: str | None = Field(default=None, min_length=2, max_length=100)
    department: str | None = Field(default=None, min_length=2, max_length=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str
    department: str

    model_config = ConfigDict(from_attributes=True)