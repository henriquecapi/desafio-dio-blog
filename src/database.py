import databases
import sqlalchemy as sa

from config import settings

database = databases.Database(settings.database_url)
metadata = sa.MetaData()

# Verifica se o banco é SQLite para aplicar argumentos específicos
if settings.database_url.startswith("sqlite"):
    engine = sa.create_engine(
        settings.database_url, connect_args={"check_same_thread": False}
    )
else:
    # Para Postgres e outros, não usamos check_same_thread
    engine = sa.create_engine(settings.database_url)
