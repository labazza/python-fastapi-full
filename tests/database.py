from fastapi.testclient import TestClient
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from app.main import app
from alembic import command

# create the _test DB first
SQLALCHEMY_DB_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    # create a fixture so i can run as many time i want test_create_user() by dropping tables
    # otherwise i would be limited by the fact that a user can't exists multiple times
    Base.metadata.drop_all(bind=engine)
    # let sqlalchemy automatically create tables (if DB is empty)

    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close


@pytest.fixture
def client(session):
    # use command if you want to use alembic
    # command.upgrade("head")
    def override_get_db():
        try:
            yield session
        finally:
            session.close

    app.dependency_overrides[get_db] = override_get_db()
    yield TestClient(app)
    # command.downgrade("base")