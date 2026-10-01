import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db


# Create a separate in-memory database for testing
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Provide the test database to the API
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


# Register a test user and obtain an authentication token
@pytest.fixture
def auth_headers(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# Sample student data
def sample_student(email="bhanu@example.com"):
    return {
        "name": "Bhanu",
        "email": email,
        "age": 21,
        "course": "B.Tech",
        "department": "AIML",
    }


def test_create_student(client, auth_headers):
    response = client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Bhanu"
    assert response.json()["email"] == "bhanu@example.com"


def test_get_students(client, auth_headers):
    client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    response = client.get(
        "/students/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_student_by_id(client, auth_headers):
    create_response = client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_update_student(client, auth_headers):
    create_response = client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={"course": "M.Tech"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["course"] == "M.Tech"


def test_delete_student(client, auth_headers):
    create_response = client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/students/{student_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_duplicate_email(client, auth_headers):
    client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    response = client.post(
        "/students/",
        json=sample_student(),
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_student_not_found(client, auth_headers):
    response = client.get(
        "/students/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404