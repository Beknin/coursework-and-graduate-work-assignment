from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from datetime import date


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    course = Column(Integer, nullable=False)
    group_name = Column(String)
    
    enrollments = relationship("Enrollment", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    position = Column(String)
    degree = Column(String)
    contact = Column(String)
    
    topics = relationship("Topic", back_populates="teacher")


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(Date, default=date.today)
    
    teacher = relationship("Teacher", back_populates="topics")
    enrollments = relationship("Enrollment", back_populates="topic")


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String, default="pending")  # pending, confirmed, rejected
    confirmed_at = Column(Date)
    
    student = relationship("Student", back_populates="enrollments")
    topic = relationship("Topic", back_populates="enrollments")


class Deadline(Base):
    __tablename__ = "deadlines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_active = Column(Integer, default=1)  # 1 = активен, 0 = неактивен