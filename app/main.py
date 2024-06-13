from fastapi import FastAPI
from app.database import engine, Base
from app.controllers import task_controller

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task_controller.router)
