from sqlmodel import SQLModel , create_engine, Session
from dotenv import load_dotenv
from typing import Generator
import os

load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL")
connect_args = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, 
                       connect_args =  connect_args, 
                       echo = True,
                       pool_pre_ping=True,  # Verify connections before using them
                       pool_recycle=3600,   # Recycle connections after 1 hour
                       pool_size=5,         # Number of connections to maintain
                       max_overflow=10
                       )

def init_db():
    from app.models.ticket import Ticket
    from app.models.user import User
    from app.models.ChatMessage import ChatMessage
   
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a DB session per request.
    """
    with Session(engine) as session:
        yield session




