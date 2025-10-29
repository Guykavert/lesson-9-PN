from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Базовая модель
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

class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
