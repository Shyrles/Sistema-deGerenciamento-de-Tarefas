from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.repositories import task_repository

def create_task(db: Session, title: str, description: str, status: str):
    task = Task(title=title, description=description, status=status)
    return task_repository.create_task(db, task)

def get_task_by_id(db: Session, task_id: int):
    return task_repository.get_task_by_id(db, task_id)

def update_task(db: Session, task_id: int, title: str, description: str, status: str):
    return task_repository.update_task(db, task_id, title, description, status)

def delete_task(db: Session, task_id: int):
    return task_repository.delete_task(db, task_id)

def list_tasks(db: Session):
    return task_repository.list_tasks(db)
