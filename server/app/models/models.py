from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

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


    @classmethod
    def get_students(cls, db):
        return db.query(cls).filter(cls.role == "student").all()

    @classmethod
    def get_teachers(cls, db):
        return db.query(cls).filter(cls.role == "teacher").all()

    @classmethod
    def get_admins(cls, db):
        return db.query(cls).filter(cls.role == "admin").all()

    @classmethod
    def get_student(cls, db, user_id: int):
        return db.query(cls).filter(
            cls.id == user_id,
            cls.role == "student"
        ).first()

    @classmethod
    def get_teacher(cls, db, user_id: int):
        return db.query(cls).filter(
            cls.id == user_id,
            cls.role == "teacher"
        ).first()

    @classmethod
    def get_admin(cls, db, user_id: int):
        return db.query(cls).filter(
            cls.id == user_id,
            cls.role == "admin"
        ).first()

    @classmethod
    def get_by_role(cls, db, user_id: int, role: str):
        return db.query(cls).filter(
            cls.id == user_id,
            cls.role == role
        ).first()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "login": self.login or "",
            "role": self.role,
            "course": self.course,
            "group_name": self.group_name,
            "department": self.department,
            "position": self.position,
            "degree": self.degree,
            "contact": self.contact,
            "access_level": self.access_level,
        }

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}', role='{self.role}')>"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="free")
    created_at = Column(Date, default=date.today)

    teacher = relationship(
        "User",
        back_populates="topics",
        foreign_keys=[teacher_id]
    )
    enrollments = relationship("Enrollment", back_populates="topic")

    def to_dict(self, teacher_name: str = None) -> dict:
        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "teacher_name": teacher_name or "",
            "level": self.level,
            "title": self.title,
            "description": self.description,
            "status": self.status or "free",
            "created_at": str(self.created_at) if self.created_at else None,
        }


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String, default="pending")
    comment = Column(Text, nullable=True)
    created_at = Column(Date, default=date.today)
    confirmed_at = Column(Date, nullable=True)

    student = relationship(
        "User",
        back_populates="enrollments",
        foreign_keys=[student_id]
    )
    topic = relationship("Topic", back_populates="enrollments")

    def to_dict(self, student_name: str = None, topic_title: str = None) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": student_name or "",
            "topic_id": self.topic_id,
            "topic_title": topic_title or "",
            "status": self.status,
            "comment": self.comment,
            "created_at": str(self.created_at) if self.created_at else None,
            "confirmed_at": str(self.confirmed_at) if self.confirmed_at else None,
        }


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    date = Column(Date, nullable=False)
    is_active = Column(Integer, default=1)