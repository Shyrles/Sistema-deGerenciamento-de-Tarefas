import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repositories import task_repository
from app.models.task_model import Task
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./new_test.db"  # Corrigido para new_test.db
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
    yield
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes


@pytest.fixture(scope="function")
def db_session():
    db = SessionTesting()
    yield db
    db.close()


def test_create_task(db_session):
    task = Task(title="Test Task", description="Test Description", status="Pendente")
    created_task = task_repository.create_task(db_session, task)
    assert created_task.title == "Test Task"


def test_get_task_by_id(db_session):
    task = task_repository.get_task_by_id(db_session, task_id=1)
    assert task.id == 1


def test_update_task(db_session):
    task = task_repository.update_task(db_session, task_id=1, title="Updated Task", description="Updated Description",
                                       status="Em Progresso")
    assert task.title == "Updated Task"


def test_delete_task(db_session):
    # Primeiro, cria uma tarefa para garantir que há uma tarefa com ID 1
    task = Task(title="Test Task", description="Test Description", status="Pendente")
    task_repository.create_task(db_session, task)

    # Exclui a tarefa criada
    deleted_task = task_repository.delete_task(db_session, task_id=1)
    assert deleted_task is None

    # Verifica se a tarefa realmente foi excluída
    task = task_repository.get_task_by_id(db_session, task_id=1)
    assert task is None


def test_list_tasks(db_session):
    tasks = task_repository.list_tasks(db_session)
    assert isinstance(tasks, list)
