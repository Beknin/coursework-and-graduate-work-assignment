from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    full_name: str
    login: Optional[str] = None
    role: str  # admin, teacher, student

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int


class StudentBase(UserBase):
    course: int
    group_name: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int


class TeacherBase(UserBase):
    position: Optional[str] = None
    degree: Optional[str] = None
    contact: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int


class AdminBase(UserBase):
    access_level: str = "full"

class AdminCreate(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int


class TopicBase(BaseModel):
    teacher_id: int
    level: str
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: int
    created_at: date
    status: Optional[str] = None


class EnrollmentBase(BaseModel):
    student_id: int
    topic_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    status: str
    confirmed_at: Optional[date] = None


class DeadlineBase(BaseModel):
    name: str
    date: date
    is_active: bool = True

class DeadlineCreate(DeadlineBase):
    pass

class DeadlineResponse(DeadlineBase):
    id: int