import os
import unittest.mock
import pytest

import application.models
import application.database


@pytest.fixture
def use_db():
    db_path = "./sql_app_test.db"
    sql_db_url = f"sqlite:///{db_path}"

    application.database._engine = None
    application.database._SessionLocal = None
    with unittest.mock.patch(
        "application.database.get_sa_db_url", return_value=sql_db_url
    ):
        engine = application.database.get_engine()
        application.models.Base.metadata.create_all(engine)
        yield None
        application.models.Base.metadata.drop_all(engine)

    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def session_maker(use_db):
    sessions_list = []

    def get_session():
        session_local = application.database.get_session_local()
        session = session_local()
        sessions_list.append(session)
        return session

    yield get_session

    for session in sessions_list:
        session.close()
