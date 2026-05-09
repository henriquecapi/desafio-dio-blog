import os
import databases
import sqlalchemy as sa

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.sqlite")

# Correção para SQLAlchemy 2.0 (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# CRIAR A INSTÂNCIA DO DATABASE
database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

# Argumentos extras para o engine (ex: check_same_thread apenas para SQLite)
engine_args = {}
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = sa.create_engine(DATABASE_URL, **engine_args)
