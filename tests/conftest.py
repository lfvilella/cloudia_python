import os
import unittest.mock
import pytest

import application.models
import application.database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def use_db():
    db_path = "./sql_app_test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with unittest.mock.patch("application.database.engine", engine):
        with unittest.mock.patch(
            "application.database.SessionLocal", SessionLocal
        ):
            application.models.Base.metadata.create_all(engine)
            yield None
            application.models.Base.metadata.drop_all(engine)

    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def session_maker(use_db):
    sessions_list = []

    def get_session():
        session = application.database.SessionLocal()
        sessions_list.append(session)
        return session

    yield get_session

    for session in sessions_list:
        session.close()
