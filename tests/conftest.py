# this is a special file used by pytest any fixture defined here will be available by the tests of this package
from os import posix_fadvise

import pytest
from alembic import command
from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oath2 import create_access_token
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


@pytest.fixture()
def test_user(client):
    user_data = {"email": "pippo@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # update password with one specified above
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {"email": "pippa@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # update password with one specified above
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "awesome first post",
            "content": "blah post suca pappa ciao",
            "owner_id": test_user["id"],
        },
        {
            "title": "awesome second post",
            "content": "morem ortus coppa marty",
            "owner_id": test_user["id"],
        },
        {
            "title": "awesome third post",
            "content": "becco ninert sofu battindus",
            "owner_id": test_user["id"],
        },
        {
            "title": "awesome fourth post",
            "content": "becco ninert dksk sofu battindus",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    my_posts = session.query(models.Post).all()
    return my_posts
