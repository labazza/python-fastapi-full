import pytest
from jose import jwt
from app import schemas
from app.config import settings

# no need to import anything with conftest.py
# from .database import client, session


def test_create_user(client):
    # the trailing / is necessary because fastapi is smart enough to redirect /users to users but the return code is 307(redirect)
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_users(test_user, client):
    res = client.post(
        # data because login endpoint uses form data to login
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secrete_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail", "password123", 403),
        ("pippo@gmail.com", "wrongPassword", 403),
        ("wrongemail", "wrongpassword", 123),
        (None, "password123", 422),
        ("pippo@gmail.com", None, 422),
    ],
)
def test_invalid_login(client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
