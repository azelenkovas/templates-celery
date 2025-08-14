# database.py 
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
import logging
from templates.models.template import Template

logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

DATABASE_URL = "sqlite:///./sql_app.db" # Adjust path as needed

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    #SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)] 