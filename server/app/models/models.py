from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    role = Column(String, nullable=False)

    email = Column(String, nullable=True)

    course = Column(Integer, nullable=True)
    group_name = Column(String, nullable=True)

    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    contact = Column(String, nullable=True)

    access_level = Column(String, nullable=True, default="full")

    topics = relationship(
        "Topic",
        back_populates="teacher",
        foreign_keys="Topic.teacher_id"
    )
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        foreign_keys="Enrollment.student_id"
    )

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}', role='{self.role}')>"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(String, nullable=False)  # "coursework", "diploma"
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="free")  # "free", "assigned"
    created_at = Column(Date, default=date.today)

    teacher = relationship(
        "User",
        back_populates="topics",
        foreign_keys=[teacher_id]
    )
    enrollments = relationship("Enrollment", back_populates="topic")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String, default="pending")  # "pending", "approved", "rejected"
    comment = Column(Text, nullable=True)
    created_at = Column(Date, default=date.today)
    confirmed_at = Column(Date, nullable=True)

    student = relationship(
        "User",
        back_populates="enrollments",
        foreign_keys=[student_id]
    )
    topic = relationship("Topic", back_populates="enrollments")


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    date = Column(Date, nullable=False)
    is_active = Column(Integer, default=1)