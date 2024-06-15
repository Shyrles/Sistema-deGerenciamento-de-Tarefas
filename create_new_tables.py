from app.database import engine, Base
from app.models import Task  # Certifique-se de que o modelo Task está sendo importado
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificar a conexão com o banco de dados
try:
    with engine.connect() as connection:
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    logger.error(f"Erro ao conectar com o banco de dados: {e}")

# Adiciona um print para garantir que o modelo está registrado
print(f"Modelos registrados: {Base.metadata.tables.keys()}")

# Cria as tabelas no banco de dados
logger.info("Criando tabelas...")
Base.metadata.create_all(bind=engine)
logger.info("Tabelas criadas com sucesso.")
