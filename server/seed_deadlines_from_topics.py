# seed_deadlines_from_topics.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import openpyxl
from datetime import datetime
from app.database.db import SessionLocal
from app.models import models


def load_deadlines_from_topics(file_path: str):
    """Читает Excel с темами и создаёт дедлайны для каждой темы"""
    db = SessionLocal()
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb.active
        
        added = 0
        skipped = 0
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or not row[0]:
                continue
            
            topic_title = str(row[0]).strip()
            deadline_date = row[2]  # колонка C
            
            if not deadline_date:
                print(f"⏭️ Нет даты для: {topic_title}")
                skipped += 1
                continue
            
            # Преобразуем дату
            if isinstance(deadline_date, datetime):
                deadline_date = deadline_date.date()
            elif isinstance(deadline_date, str):
                try:
                    deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date()
                except ValueError:
                    print(f"⚠️ Неверный формат даты: {deadline_date}")
                    skipped += 1
                    continue
            
            # Ищем тему по названию
            topic = db.query(models.Topic).filter(
                models.Topic.title == topic_title
            ).first()
            
            if not topic:
                print(f"⚠️ Тема не найдена: {topic_title}")
                skipped += 1
                continue
            
            # Создаём дедлайн для этой темы
            deadline_name = f"topic_{topic.id}_deadline"
            existing = db.query(models.Deadline).filter(
                models.Deadline.name == deadline_name
            ).first()
            
            if existing:
                print(f"⏭️ Дедлайн уже существует для: {topic_title}")
                skipped += 1
                continue
            
            deadline = models.Deadline(
                name=deadline_name,
                date=deadline_date,
                is_active=1
            )
            db.add(deadline)
            added += 1
            print(f"✅ Дедлайн для темы {topic.id} ({topic_title[:30]}...): {deadline_date}")
        
        db.commit()
        print(f"\n🎉 ДОБАВЛЕНО: {added} дедлайнов")
        print(f"⏭️ ПРОПУЩЕНО: {skipped}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    file_path = "uploads/Tems.xlsx"
    load_deadlines_from_topics(file_path)