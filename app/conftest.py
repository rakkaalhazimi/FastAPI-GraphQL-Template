import pytest

import sqlite3

from fastapi.testclient import TestClient

from app.main import app, db_conn



@pytest.fixture(scope="session")
def schema_sql():
    """Returns the SQL to initialize the database."""
    return """
    CREATE TABLE item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NULL
    );
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NULL,
        email TEXT NULL,
        password TEXT NOT NULL
    );
    """

@pytest.fixture
def db_session(schema_sql):
    """Creates a fresh in-memory database for each test."""
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(schema_sql)
    connection.commit()
    yield connection
    connection.close()

@pytest.fixture
def client(db_session):
    """Overrides the FastAPI dependency and returns a TestClient."""
    def _get_test_db():
        return db_session

    app.dependency_overrides[db_conn] = _get_test_db
    with TestClient(app) as c:
        yield c
    # Clear overrides so it doesn't leak into other tests
    app.dependency_overrides.clear()