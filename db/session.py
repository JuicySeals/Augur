from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from contextlib import contextmanager
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Base(DeclarativeBase):
    pass

engine = create_engine(os.getenv('DATABASE_URL'))

SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()