import unittest.mock
import pytest
import uuid

from application import services


@pytest.fixture
def mock_bot_facebook():
    data = {
        "access": str(uuid.uuid4()),
        "verify": str(uuid.uuid4()),
    }
    with unittest.mock.patch("requests.post"):
        with unittest.mock.patch.object(
            services.FacebookBot,
            "_get_access_token",
            return_value=data["access"],
        ):
            with unittest.mock.patch.object(
                services.FacebookBot,
                "_get_verify_token",
                return_value=data["verify"],
            ):
                yield data


@pytest.fixture
def mock_bot_telegram():
    access = "1192916972:AAEvZGLAeZbpMzcuTLwdc_tQheHJ0a-P35M"  # tester bot
    fake_url = "https://fakeurl.com/telegram/bot"

    with unittest.mock.patch("requests.post"):
        with unittest.mock.patch.object(
            services.TelegramBot, "_get_access_token", return_value=access
        ):
            with unittest.mock.patch.object(
                services.TelegramBot,
                "_get_local_bot_endpoint",
                return_value=fake_url,
            ):
                yield access
