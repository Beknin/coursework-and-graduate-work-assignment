from pydantic import BaseModel
from datetime import date
from typing import Optional


# ===== USER =====
class UserBase(BaseModel):
    full_name: str
    role: str  # admin, teacher, student

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int


# ===== STUDENT (наследует User) =====
class StudentBase(UserBase):
    course: int
    group_name: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int


# ===== TEACHER (наследует User) =====
class TeacherBase(UserBase):
    position: Optional[str] = None
    degree: Optional[str] = None
    contact: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int


# ===== ADMIN (наследует User) =====
class AdminBase(UserBase):
    access_level: str = "full"

class AdminCreate(AdminBase):
    pass

class AdminResponse(AdminBase):
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