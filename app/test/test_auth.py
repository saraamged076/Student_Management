from fastapi.testclient import TestClient
from app import auth
from app.main import app

client = TestClient(app)


def get_student_token():

    # register student
    client.post(
        "/auth/register",
        json={
            "username": "sawa",
            "email": "sawa@example.com",
            "password": "sawa123",
            "role": "student"
        }
    )

    # login
    response = client.post(
        "/auth/login",
        data={
            "username": "sawa",
            "password": "sawa123"
        }
    )

    print(response.json())

    token = response.json()["access_token"]

    return token


def test_student_cannot_access_admin():

    token = get_student_token()

    response = client.get(
        "/auth/admin-only",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    
def test_duplicate_register():

    # first register
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup@example.com",
            "password": "123456",
            "role": "student"
        }
    )

    # second register
    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup2@example.com",
            "password": "123456",
            "role": "student"
        }
    )

    assert response.status_code == 409