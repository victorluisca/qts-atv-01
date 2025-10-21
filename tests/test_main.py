from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_read():
    response = client.get("/alunos/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 0, "name": "Victor", "email": "victor@gmail.com"},
        {"id": 1, "name": "Gilmar", "email": "gilmar@gmail.com"},
    ]


def test_read_by_id_success():
    id = 0
    response = client.get(f"/alunos/{id}")
    assert response.status_code == 200
    assert response.json() == {"id": 0, "name": "Victor", "email": "victor@gmail.com"}


def test_read_by_id_failure():
    id = 2
    response = client.get(f"/alunos/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_create_success():
    response = client.post(
        "/alunos/", json={"name": "Lucas", "email": "lucas@gmail.com"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 2, "name": "Lucas", "email": "lucas@gmail.com"}


def test_create_failure():
    response = client.post("/alunos/", json={"name": "Asher"})
    assert response.status_code == 422
