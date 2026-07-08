import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

RAW_CONNECTION_STRING = os.environ.get("SQL_CONNECTION_STRING", "")

if not RAW_CONNECTION_STRING:
    raise RuntimeError("SQL_CONNECTION_STRING environment variable is not set")

if RAW_CONNECTION_STRING.startswith("mssql+pyodbc"):
    # Already a full SQLAlchemy URL.
    SQLALCHEMY_DATABASE_URL = RAW_CONNECTION_STRING
else:
    # Raw ODBC connection string (e.g. from Key Vault) - wrap it for pyodbc.
    params = urllib.parse.quote_plus(RAW_CONNECTION_STRING)
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
