import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base


load_dotenv()


@pytest.fixture(scope="session")
def database_engine():
    connection_string = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/test_db"
    )

    engine = create_engine(connection_string)

    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def db_session(database_engine):
    connection = database_engine.connect()

    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
