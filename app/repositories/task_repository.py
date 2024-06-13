from sqlalchemy.orm import Session
from app.models.task_model import Task

def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, title: str, description: str, status: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = title
        task.description = description
        task.status = status
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task

def list_tasks(db: Session):
    return db.query(Task).all()
