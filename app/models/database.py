from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Criar ligação SQLite
DATABASE_URL = "sqlite:///inventario.db"


# Engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)


# Sessão
SessionLocal = sessionmaker(
    bind=engine
)


# Base para modelos
Base = declarative_base()