from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./market_system.db" #usando sqlite

#cria a engine do SQLALCHEMY
engine = create_engine(
    SQLALCHEMY_DATABASE_URL ,
    connect_args = {"check_same_thread": False}
)

