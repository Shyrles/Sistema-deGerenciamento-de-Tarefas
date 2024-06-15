from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base  # Importar Base de app/database.py

class Task(Base):
    __tablename__ = "task_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="Pendente")
    created_at = Column(DateTime, default=datetime.utcnow)
