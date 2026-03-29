from contextlib import contextmanager
import sqlite3

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings



# SQLite Database Connection
def db_conn():
    sqlite_file_name = settings.sqlite_db_name
    conn = sqlite3.connect(sqlite_file_name, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NULL
    );
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NULL,
        email TEXT NULL,
        password TEXT NOT NULL
    );                 
    """)
    conn.commit()


# SQLAlchemy
engine = create_engine(f"sqlite:///{settings.sqlite_db_name}")
Base = declarative_base()
SQLSession = sessionmaker(bind=engine)


def get_db():
    session = SQLSession()
    try:
        yield session
    except Exception as error:
        session.rollback()
        raise error
    finally:
        session.close()

@contextmanager
def session_scope():
    session = SQLSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()