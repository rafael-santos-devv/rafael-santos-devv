from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Pegando a URL do banco de variável de ambiente (seguro)
DATABASE_URL = os.getenv(
    "DATABASE_URL"
    )

# Criar engine para PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

def create_database():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
