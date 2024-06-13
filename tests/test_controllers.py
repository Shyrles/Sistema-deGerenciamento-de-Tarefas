import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Use a fixture para criar e remover tabelas antes e depois dos testes
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
    yield
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description", "status": "Pendente"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_task():
    response = client.put("/tasks/1", json={"title": "Updated Task", "description": "Updated Description", "status": "Em Progresso"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() is None
