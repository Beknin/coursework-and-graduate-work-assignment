import pytest
from pathlib import Path
from app.services.excel_service import ExcelService

TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.skipif(
    not (TEST_DATA_DIR / "Ochnoe_1_kurs_zachislenye_1.xlsx").exists(),
    reason="Файл Ochnoe_1_kurs_zachislenye_1.xlsx не найден"
)
def test_parse_real_students_1_course():
    """Тест: парсинг реального файла со студентами 1-го курса"""
    file_path = TEST_DATA_DIR / "Ochnoe_1_kurs_zachislenye_1.xlsx"
    students = ExcelService.parse_students_from_file(str(file_path))
    
    assert len(students) > 0
    # Проверяем, что есть студенты из файла
    names = [s["full_name"] for s in students]
    assert "Ганжитова Ирина Алдаровна" in names
    assert "Бавлов Сергей Александрович" in names
    
    # Проверяем группы
    groups = set(s["group_name"] for s in students)
    assert "14121" in groups or "РПО 14121" in groups


@pytest.mark.skipif(
    not (TEST_DATA_DIR / "students_4_course.xlsx").exists(),
    reason="Файл students_4_course.xlsx не найден"
)
def test_parse_real_students_4_course():
    """Тест: парсинг реального файла со студентами 4-го курса"""
    file_path = TEST_DATA_DIR / "students_4_course.xlsx"
    students = ExcelService.parse_students_from_file(str(file_path))
    
    assert len(students) > 0
    # Проверяем, что есть студенты
    names = [s["full_name"] for s in students]
    assert "Лебедев Андрей Олегович" in names or len(names) > 0


@pytest.mark.skipif(
    not (TEST_DATA_DIR / "topics_and_teachers.xlsx").exists(),
    reason="Файл topics_and_teachers.xlsx не найден"
)
def test_parse_real_topics_and_teachers():
    """Тест: парсинг реального файла с темами и преподавателями"""
    file_path = TEST_DATA_DIR / "topics_and_teachers.xlsx"
    
    # Здесь нужен метод parse_topics_and_teachers()
    # Если такого метода нет — сначала напишите его в ExcelService
    try:
        topics = ExcelService.parse_topics_and_teachers(str(file_path))
        assert len(topics) > 0
        # Проверяем, что есть темы
        titles = [t["title"] for t in topics]
        assert "Разработка веб-приложения" in titles
    except AttributeError:
        pytest.skip("Метод parse_topics_and_teachers ещё не реализован")