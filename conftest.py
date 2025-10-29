import pytest
import os
from dotenv import load_dotenv
from database import Database, Subject, Student, User

# Загрузка переменных окружения
load_dotenv()

@pytest.fixture(scope="session")
def database():
    # Получаем строку подключения из переменных окружения или используем дефолтную
    connection_string = os.getenv(
        "DATABASE_URL", 
        "postgresql://myuser:mypassword@localhost:5432/mydatabase"
    )
    db = Database(connection_string)
    return db

@pytest.fixture(scope="function")
def db_session(database):
    session = database.get_session()
    try:
        yield session
    finally:
        # Очистка после каждого теста
        session.rollback()
        session.close()
