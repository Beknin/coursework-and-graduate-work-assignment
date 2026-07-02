from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import date


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=True)
    role = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }


class Student(User):
    __tablename__ = "students"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course = Column(Integer, nullable=False)
    group_name = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    
    enrollments = relationship("Enrollment", back_populates="student")


class Teacher(User):
    __tablename__ = "teachers"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    position = Column(String)
    degree = Column(String)
    contact = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }
    
    topics = relationship("Topic", back_populates="teacher")


class Admin(User):
    __tablename__ = "admins"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    access_level = Column(String, default="full")
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(Date, default=date.today)
    
    teacher = relationship("Teacher", back_populates="topics")
    enrollments = relationship("Enrollment", back_populates="topic")  # ← ИСПРАВЛЕНО!


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String, default="pending")
    confirmed_at = Column(Date)
    
    student = relationship("Student", back_populates="enrollments")
    topic = relationship("Topic", back_populates="enrollments")  # ← ИСПРАВЛЕНО!


class Deadline(Base):
    __tablename__ = "deadlines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    date = Column(Date, nullable=False)
    is_active = Column(Integer, default=1)