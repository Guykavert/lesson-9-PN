from sqlalchemy import text
from database import Subject, Student, User


class TestDatabaseOperations:

    def test_add_subject(self, db_session):
        new_subject = Subject(
            subject_id=999,
            subject_title="Тестовый предмет",
            is_deleted=False
        )
        db_session.add(new_subject)
        db_session.commit()
        saved_subject = db_session.query(Subject).filter(
            Subject.subject_id == 999
        ).first()
        assert saved_subject is not None
        assert saved_subject.subject_title == "Тестовый предмет"
        assert saved_subject.is_deleted is False

    def test_update_subject(self, db_session):
        test_subject = Subject(
            subject_id=998,
            subject_title="Старое название",
            is_deleted=False
        )
        db_session.add(test_subject)
        db_session.commit()
        subject_to_update = db_session.query(Subject).filter(
            Subject.subject_id == 998
        ).first()
        subject_to_update.subject_title = "Новое название"
        db_session.commit()
        updated_subject = db_session.query(Subject).filter(
            Subject.subject_id == 998
        ).first()
        assert updated_subject.subject_title == "Новое название"

    def test_soft_delete_student(self, db_session):
        test_student = Student(
            student_id=997,
            user_id=10001,
            education_form="Очная",
            is_deleted=False
        )
        db_session.add(test_student)
        db_session.commit()
        created_student = db_session.query(Student).filter(
            Student.student_id == 997
        ).first()
        assert created_student.is_deleted is False
        student_to_delete = db_session.query(Student).filter(
            Student.student_id == 997
        ).first()
        student_to_delete.is_deleted = True
        db_session.commit()
        deleted_student = db_session.query(Student).filter(
            Student.student_id == 997
        ).first()
        assert deleted_student.is_deleted is True


class TestComplexOperations:

    def test_add_and_verify_user(self, db_session):
        new_user = User(
            user_id=10002,
            user_email="test.user@example.com",
            is_deleted=False
        )
        db_session.add(new_user)
        db_session.commit()
        saved_user = db_session.query(User).filter(
            User.user_email == "test.user@example.com"
        ).first()
        assert saved_user is not None
        assert saved_user.user_id == 10002


def test_database_connection(db_session):
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
