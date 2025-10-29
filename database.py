from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(Integer, primary_key=True)
    subject_title = Column(String(255))
    is_deleted = Column(Boolean, default=False)


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    education_form = Column(String(100))
    is_deleted = Column(Boolean, default=False)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String(255))
    is_deleted = Column(Boolean, default=False)
