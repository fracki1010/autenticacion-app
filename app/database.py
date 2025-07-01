from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

from app.core.config import settings

# Construcción de la URL de la base de datos usando la configuración centralizada
#DATABASE_URL = f"mysql+pymysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

DATABASE_URL = "mysql+pymysql://usuario:123456@localhost:3308/test"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
