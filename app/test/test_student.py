from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_admin_token():

    # register admin
    client.post(
        "/auth/register",
        json={
            "username": "admin1",
            "email": "admin1@test.com",
            "password": "admin123",
            "role": "admin"
        }
    )

    # login
    response = client.post(
        "/auth/login",
        data={
            "username": "admin1",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return token

def create_student(token):

    response = client.post(
        "/students/",
        json={
            "name": "Ali",
            "department": "CS",
            "gpa": 3.5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response.json()

def test_create_student():

    token = get_admin_token()

    response = client.post(
        "/students/",
        json={
            "name": "Ahmed",
            "department": "IT",
            "gpa": 3.2
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_students():

    response = client.get("/students/")

    assert response.status_code == 200


def test_update_student():

    token = get_admin_token()

    student = create_student(token)

    response = client.put(
        f"/students/{student['id']}",
        json={
            "name": "Updated",
            "department": "AI",
            "gpa": 3.9
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_delete_student():

    token = get_admin_token()

    student = create_student(token)

    response = client.delete(
        f"/students/{student['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    
def test_get_invalid_student():

    response = client.get("/students/9999")

    assert response.status_code == 404    