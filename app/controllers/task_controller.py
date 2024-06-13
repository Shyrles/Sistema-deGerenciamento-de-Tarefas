from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services import task_service

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str

router = APIRouter()

@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.title, task.description, task.status)

@router.get("/tasks/")
def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)

@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, task.title, task.description, task.status)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(db, task_id)
