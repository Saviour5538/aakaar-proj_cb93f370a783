import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from contextlib import contextmanager
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# SQLAlchemy engine configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Base class for models
class Base(DeclarativeBase):
    pass

def get_db():
    """Dependency for FastAPI database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()