# check_data.py
from app.database.db import SessionLocal
from app.models import models

db = SessionLocal()

students = db.query(models.User).filter(models.User.role == 'student').count()
teachers = db.query(models.User).filter(models.User.role == 'teacher').count()
topics = db.query(models.Topic).count()
deadlines = db.query(models.Deadline).all()

print(f'👨‍🎓 Студентов: {students}')
print(f'👨‍🏫 Преподавателей: {teachers}')
print(f'📚 Тем: {topics}')

if deadlines:
    for d in deadlines:
        print(f'{d.name}: {d.date} (активен: {d.is_active})')
else:
    print('❌ Дедлайнов нет!')

db.close()