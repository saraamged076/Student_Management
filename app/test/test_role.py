from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_student_token():
    # login
    response = client.post(
        "/auth/login",
        data={
            "username": "sawa",
            "password": "sawa123"
        }
    )

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
    
def test_invalid_login():

    response = client.post(
        "/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401        