import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Criação do engine e da sessão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definição de metadados e criação de tabela temporária
metadata = MetaData()
test_table = Table(
    'test_table', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False)
)

# Cria a tabela no banco de dados
metadata.create_all(engine)


# Insere um registro na tabela
def test_sqlalchemy():
    session = SessionLocal()
    try:
        # Insere um registro
        insert_stmt = test_table.insert().values(name="Test Name")
        session.execute(insert_stmt)
        session.commit()

        # Consulta o registro inserido
        select_stmt = test_table.select()
        result = session.execute(select_stmt).fetchall()
        for row in result:
            print(f"id: {row['id']}, name: {row['name']}")
    finally:
        session.close()


# Executa o teste
if __name__ == "__main__":
    test_sqlalchemy()

    # Limpa a tabela depois do teste
    metadata.drop_all(engine)
