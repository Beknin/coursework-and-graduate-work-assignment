# check.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.database.db import SessionLocal
from app.models import models


def check_database():
    db = SessionLocal()
    
    print("=" * 60)
    print("📊 ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # ===== 1. Пользователи =====
    users = db.query(models.User).all()
    print(f"\n👥 ВСЕГО ПОЛЬЗОВАТЕЛЕЙ: {len(users)}")
    
    admins = db.query(models.User).filter(models.User.role == 'admin').count()
    students = db.query(models.User).filter(models.User.role == 'student').count()
    teachers = db.query(models.User).filter(models.User.role == 'teacher').count()
    print(f"   👨‍💼 Админов: {admins}")
    print(f"   👨‍🎓 Студентов: {students}")
    print(f"   👨‍🏫 Преподавателей: {teachers}")
    
    # ===== 2. Студенты (если есть таблица) =====
    if hasattr(models, "Student"):
        student_records = db.query(models.Student).count()
        print(f"\n📚 СТУДЕНТЫ (с доп. данными): {student_records}")
    
    # ===== 3. Преподаватели (если есть таблица) =====
    if hasattr(models, "Teacher"):
        teacher_records = db.query(models.Teacher).count()
        print(f"\n📚 ПРЕПОДАВАТЕЛИ (с доп. данными): {teacher_records}")
    
    # ===== 4. Темы =====
    topics = db.query(models.Topic).all()
    print(f"\n📚 ВСЕГО ТЕМ: {len(topics)}")
    
    if topics:
        print("\n📋 СПИСОК ВСЕХ ТЕМ:")
        print("-" * 80)
        for t in topics:
            # Получаем имя преподавателя
            teacher = db.query(models.User).filter(models.User.id == t.teacher_id).first()
            teacher_name = teacher.full_name if teacher else "Неизвестно"
            print(f"  ID {t.id:2d}: {t.title[:45]:45s} | {teacher_name[:20]:20s} | {t.level:10s} | {t.status}")
    else:
        print("  ❌ Тем нет!")
    
    # ===== 5. Записи (Enrollments) =====
    enrollments = db.query(models.Enrollment).all()
    print(f"\n📝 ВСЕГО ЗАПИСЕЙ: {len(enrollments)}")
    
    if enrollments:
        print("\n📋 СПИСОК ЗАПИСЕЙ:")
        print("-" * 80)
        for e in enrollments:
            student = db.query(models.User).filter(models.User.id == e.student_id).first()
            topic = db.query(models.Topic).filter(models.Topic.id == e.topic_id).first()
            student_name = student.full_name if student else "Неизвестно"
            topic_title = topic.title if topic else "Неизвестно"
            print(f"  ID {e.id:2d}: {student_name[:25]:25s} -> {topic_title[:35]:35s} | {e.status}")
    
    # ===== 6. Дедлайны =====
    deadlines = db.query(models.Deadline).all()
    print(f"\n📅 ВСЕГО ДЕДЛАЙНОВ: {len(deadlines)}")
    
    if deadlines:
        print("\n📋 СПИСОК ДЕДЛАЙНОВ:")
        print("-" * 80)
        for d in deadlines:
            active = "✅" if d.is_active else "❌"
            print(f"  {d.name:30s} -> {d.date} {active}")
    else:
        print("  ❌ Дедлайнов нет!")
    
    # ===== 7. Последние 5 студентов =====
    print("\n👨‍🎓 ПОСЛЕДНИЕ 5 СТУДЕНТОВ:")
    print("-" * 80)
    last_students = db.query(models.User).filter(models.User.role == 'student').order_by(models.User.id.desc()).limit(5).all()
    for s in last_students:
        print(f"  {s.id:3d}: {s.full_name} (логин: {s.login})")
    
    # ===== 8. Последние 5 преподавателей =====
    print("\n👨‍🏫 ПОСЛЕДНИЕ 5 ПРЕПОДАВАТЕЛЕЙ:")
    print("-" * 80)
    last_teachers = db.query(models.User).filter(models.User.role == 'teacher').order_by(models.User.id.desc()).limit(5).all()
    for t in last_teachers:
        print(f"  {t.id:3d}: {t.full_name} (логин: {t.login})")
    
    print("\n" + "=" * 60)
    print("✅ ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 60)
    
    db.close()


if __name__ == "__main__":
    check_database()