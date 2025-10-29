import pytest
from database import Subject, Student, User

class TestDatabaseOperations:
    """Тесты для операций с базой данных"""
    
    def test_add_subject(self, db_session):
        """Тест добавления нового предмета"""
        # Подготовка данных
        new_subject = Subject(
            subject_id=999,
            subject_title="Тестовый предмет",
            is_deleted=False
        )
        
        # Выполнение операции
        db_session.add(new_subject)
        db_session.commit()
        
        # Проверка результата
        saved_subject = db_session.query(Subject).filter(
            Subject.subject_id == 999
        ).first()
        
        assert saved_subject is not None
        assert saved_subject.subject_title == "Тестовый предмет"
        assert saved_subject.is_deleted == False
        
        # Очистка
        db_session.query(Subject).filter(Subject.subject_id == 999).delete()
        db_session.commit()
    
    def test_update_subject(self, db_session):
        """Тест изменения названия предмета"""
        # Сначала создаем тестовый предмет
        test_subject = Subject(
            subject_id=998,
            subject_title="Старое название",
            is_deleted=False
        )
        db_session.add(test_subject)
        db_session.commit()
        
        # Изменяем предмет
        db_session.query(Subject).filter(
            Subject.subject_id == 998
        ).update({"subject_title": "Новое название"})
        db_session.commit()
        
        # Проверка изменения
        updated_subject = db_session.query(Subject).filter(
            Subject.subject_id == 998
        ).first()
        
        assert updated_subject.subject_title == "Новое название"
        
        # Очистка
        db_session.query(Subject).filter(Subject.subject_id == 998).delete()
        db_session.commit()
    
    def test_soft_delete_student(self, db_session):
        """Тест мягкого удаления студента"""
        # Создаем тестового студента
        test_student = Student(
            student_id=997,
            user_id=10001,
            education_form="Очная",
            is_deleted=False
        )
        db_session.add(test_student)
        db_session.commit()
        
        # Мягкое удаление
        db_session.query(Student).filter(
            Student.student_id == 997
        ).update({"is_deleted": True})
        db_session.commit()
        
        # Проверка мягкого удаления
        deleted_student = db_session.query(Student).filter(
            Student.student_id == 997
        ).first()
        
        assert deleted_student.is_deleted == True
        
        # Проверка, что запись все еще существует в БД
        all_students = db_session.query(Student).filter(
            Student.student_id == 997
        ).all()
        
        assert len(all_students) == 1
        
        # Очистка - полное удаление тестовых данных
        db_session.query(Student).filter(Student.student_id == 997).delete()
        db_session.commit()

class TestComplexOperations:
    """Тесты для более сложных операций"""
    
    def test_add_and_verify_user(self, db_session):
        """Тест добавления пользователя и проверки его данных"""
        # Добавление пользователя
        new_user = User(
            user_id=10002,
            user_email="test.user@example.com",
            is_deleted=False
        )
        db_session.add(new_user)
        db_session.commit()
        
        # Проверка через запрос
        saved_user = db_session.query(User).filter(
            User.user_email == "test.user@example.com"
        ).first()
        
        assert saved_user is not None
        assert saved_user.user_id == 10002
        
        # Очистка
        db_session.query(User).filter(User.user_id == 10002).delete()
        db_session.commit()

def test_cleanup_verification(db_session):
    """Дополнительный тест для проверки очистки данных"""
    # Проверяем, что тестовые данные были удалены
    test_subject_999 = db_session.query(Subject).filter(
        Subject.subject_id == 999
    ).first()
    test_subject_998 = db_session.query(Subject).filter(
        Subject.subject_id == 998
    ).first()
    test_student_997 = db_session.query(Student).filter(
        Student.student_id == 997
    ).first()
    test_user_10002 = db_session.query(User).filter(
        User.user_id == 10002
    ).first()
    
    assert test_subject_999 is None
    assert test_subject_998 is None
    assert test_student_997 is None
    assert test_user_10002 is None
