# seed_topics_and_teachers.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import openpyxl
from app.database.db import SessionLocal
from app.models import models
from app.core.security import hash_password


def load_topics_and_teachers(file_path: str):
    db = SessionLocal()
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb.active
        
        added_topics = 0
        added_teachers = 0
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row:
                continue
            
            topic_title = row[0]
            teacher_name = row[1]
            
            if not topic_title or not teacher_name:
                continue
            
            # Проверяем, есть ли уже такой преподаватель
            teacher = db.query(models.User).filter(
                models.User.full_name == teacher_name,
                models.User.role == "teacher"
            ).first()
            
            if not teacher:
                # Создаём преподавателя
                login = teacher_name.split()[0].lower()
                
                # Проверяем, не занят ли логин
                existing_login = db.query(models.User).filter(
                    models.User.login == login
                ).first()
                
                if existing_login:
                    # Если логин занят, добавляем номер
                    login = f"{login}_{added_teachers + 1}"
                
                user = models.User(
                    full_name=teacher_name,
                    login=login,
                    hashed_password=hash_password("password"),
                    role="teacher"
                )
                db.add(user)
                db.flush()
                
                if hasattr(models, "Teacher"):
                    teacher_obj = models.Teacher(
                        id=user.id,
                        position="Преподаватель",
                        degree="",
                        contact=""
                    )
                    db.add(teacher_obj)
                
                teacher = user
                added_teachers += 1
                print(f"✅ Добавлен преподаватель: {teacher_name} (логин: {login})")
            else:
                print(f"⏭️ Преподаватель уже существует: {teacher_name}")
            
            # Проверяем, есть ли уже такая тема
            existing_topic = db.query(models.Topic).filter(
                models.Topic.title == topic_title
            ).first()
            
            if existing_topic:
                print(f"⏭️ Пропущена тема: {topic_title} (уже существует)")
                continue
            
            topic = models.Topic(
                teacher_id=teacher.id,
                level="Курсовая",
                title=topic_title,
                description="",
                status="free"
            )
            db.add(topic)
            added_topics += 1
            print(f"✅ Добавлена тема: {topic_title} (преподаватель: {teacher_name})")
        
        db.commit()
        print(f"\n🎉 ДОБАВЛЕНО: {added_teachers} преподавателей, {added_topics} тем")
        
    except Exception as e:
        db.rollback()
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    file_path = "uploads/topics_and_teachers.xlsx"
    load_topics_and_teachers(file_path)