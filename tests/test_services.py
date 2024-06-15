import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services import task_service
from app.database import Base
from app.models.task_model import Task

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
    task = task_service.create_task(db_session, title="Test Task", description="Test Description", status="Pendente")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "Pendente"


def test_get_task_by_id(db_session):
    # Primeiro, cria uma tarefa para garantir que há uma tarefa com ID 1
    new_task = task_service.create_task(db_session, title="Test Task", description="Test Description",
                                        status="Pendente")
    task = task_service.get_task_by_id(db_session, task_id=new_task.id)
    assert task.id == new_task.id
    assert task.title == new_task.title
    assert task.description == new_task.description
    assert task.status == new_task.status


def test_update_task(db_session):
    # Primeiro, cria uma tarefa para garantir que há uma tarefa com ID 1
    new_task = task_service.create_task(db_session, title="Test Task", description="Test Description",
                                        status="Pendente")
    updated_task = task_service.update_task(db_session, task_id=new_task.id, title="Updated Task",
                                            description="Updated Description", status="Em Progresso")
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.status == "Em Progresso"


def test_delete_task(db_session):
    # Primeiro, cria uma tarefa para garantir que há uma tarefa com ID 1
    new_task = task_service.create_task(db_session, title="Test Task", description="Test Description",
                                        status="Pendente")
    task_service.delete_task(db_session, task_id=new_task.id)
    task = task_service.get_task_by_id(db_session, task_id=new_task.id)
    assert task is None


def test_list_tasks(db_session):
    # Limpa a tabela para garantir que começamos com uma lista vazia
    db_session.query(Task).delete()
    db_session.commit()

    # Adiciona algumas tarefas para listar
    task_service.create_task(db_session, title="Task 1", description="Description 1", status="Pendente")
    task_service.create_task(db_session, title="Task 2", description="Description 2", status="Concluído")
    tasks = task_service.list_tasks(db_session)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
