from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import USER_DB_PATH
from .models import Base

DATABASE_URL = f"sqlite:///{USER_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
