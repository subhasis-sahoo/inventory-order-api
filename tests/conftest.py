import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base

from fastapi.testclient import TestClient

from app.main import app
from app.database.dependencies import get_db

from dotenv import load_dotenv
import os


load_dotenv()


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not set")



test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)



@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()