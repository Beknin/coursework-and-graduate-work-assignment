from pydantic import BaseModel
from datetime import date
from typing import Optional


# ===== USER =====
class UserBase(BaseModel):
    full_name: str
    login: str
    role: str  # admin, teacher, student

class UserCreate(UserBase):
    course: Optional[int] = None
    group_name: Optional[str] = None
    position: Optional[str] = None
    degree: Optional[str] = None
    contact: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int


# ===== STUDENT =====
class StudentBase(UserBase):
    course: int
    group_name: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int


# ===== TEACHER =====
class TeacherBase(UserBase):
    position: Optional[str] = None
    degree: Optional[str] = None
    contact: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int


# ===== TOPIC =====
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


# ===== ENROLLMENT =====
class EnrollmentBase(BaseModel):
    student_id: int
    topic_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    status: str
    confirmed_at: Optional[date] = None


# ===== DEADLINE =====
class DeadlineBase(BaseModel):
    name: str
    date: date
    is_active: bool = True

class DeadlineCreate(DeadlineBase):
    pass

class DeadlineResponse(DeadlineBase):
    id: int