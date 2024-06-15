import logging
from fastapi import FastAPI
from app.database import engine, Base
from app.models.task_model import Task  # Certifique-se de importar os modelos aqui

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

from app.controllers import task_controller  # Importar os controladores após inicializar o FastAPI
app.include_router(task_controller.router)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Start request path={request.url.path}")
    response = await call_next(request)
    logger.info(f"Completed request path={request.url.path} status={response.status_code}")
    return response
