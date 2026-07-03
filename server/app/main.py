from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import topics, students, teachers, enrollments, orders, admin, auth
from app.database import db
from app.models import models

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI(
    title="Система распределения тем ВКР",
    version="1.0.0",
    redoc_url="/redoc",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(topics.router, prefix="/api/topics", tags=["Темы"])
app.include_router(students.router, prefix="/api/students", tags=["Студенты"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["Преподаватели"])
app.include_router(enrollments.router, prefix="/api/enrollments", tags=["Записи"])
app.include_router(orders.router, prefix="/api/orders", tags=["Приказы"])
app.include_router(auth.router, prefix="/api/auth", tags=["Авторизация"])
app.include_router(auth.router, prefix="/auth", tags=["Авторизация (клиент)"])
app.include_router(admin.router, prefix="/api/admin", tags=["Администрирование"])

@app.get("/health")
def health():
    return {"status": "ok"}