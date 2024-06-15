import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# URL do banco de dados
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./new_test.db")

# Verificação de depuração para garantir que a URL foi carregada corretamente
print(f"Conectando ao banco de dados em: {SQLALCHEMY_DATABASE_URL}")

# Criação do engine e da sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

# Dependência de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
