import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services import task_service
from app.models.task_model import Task
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
    yield
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes

def test_create_task():
    db = SessionTesting()
    task = task_service.create_task(db, title="Test Task", description="Test Description", status="Pendente")
    assert task.title == "Test Task"

def test_get_task_by_id():
    db = SessionTesting()
    task = task_service.get_task_by_id(db, task_id=1)
    assert task.id == 1

def test_update_task():
    db = SessionTesting()
    task = task_service.update_task(db, task_id=1, title="Updated Task", description="Updated Description", status="Em Progresso")
    assert task.title == "Updated Task"

def test_delete_task():
    db = SessionTesting()
    task = task_service.delete_task(db, task_id=1)
    assert task is None

def test_list_tasks():
    db = SessionTesting()
    tasks = task_service.list_tasks(db)
    assert isinstance(tasks, list)
