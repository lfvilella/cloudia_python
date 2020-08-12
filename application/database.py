import os
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_sa_db_url():
    return os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")


_engine = None


def get_engine():
    global _engine
    if _engine:
        return _engine

    db_url = get_sa_db_url()
    connect_args = {}
    if db_url.startswith("sqlite:"):
        connect_args["check_same_thread"] = False

    _engine = create_engine(db_url, connect_args=connect_args)
    return _engine


_SessionLocal = None


def get_session_local():
    global _SessionLocal
    if _SessionLocal:
        return _SessionLocal

    _SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=get_engine()
    )
    return _SessionLocal


@contextlib.contextmanager
def get_db():
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
