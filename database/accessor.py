from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings

engine = create_engine(Settings().db_url, future=True, echo=True, pool_pre_ping=True)

SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db_session() -> Session:
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
