import unittest.mock
import pytest
import uuid

@pytest.fixture
def mock_bot_facebook():
    data = {
        'access': str(uuid.uuid4()),
        'verify': str(uuid.uuid4()),
    }
    with unittest.mock.patch("requests.post"):
        with unittest.mock.patch("application.bot_facebook._get_access_token", return_value=data['access']):
            with unittest.mock.patch("application.bot_facebook._get_verify_token", return_value=data['verify']):
                yield data
