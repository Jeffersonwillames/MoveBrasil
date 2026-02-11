"""Configuração de banco de dados SQLite para o projeto MoveBrasil."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./movebrasil.db"

# check_same_thread=False é necessário para acesso concorrente no FastAPI com SQLite.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco para cada requisição e garante fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
