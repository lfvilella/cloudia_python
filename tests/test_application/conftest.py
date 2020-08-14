import unittest.mock
import pytest
import uuid

from application import bot_telegram


@pytest.fixture
def mock_bot_facebook():
    data = {
        "access": str(uuid.uuid4()),
        "verify": str(uuid.uuid4()),
    }
    with unittest.mock.patch("requests.post"):
        with unittest.mock.patch(
            "application.bot_facebook._get_access_token",
            return_value=data["access"],
        ):
            with unittest.mock.patch(
                "application.bot_facebook._get_verify_token",
                return_value=data["verify"],
            ):
                yield data


@pytest.fixture
def mock_bot_telegram():
    access = "1192916972:AAEvZGLAeZbpMzcuTLwdc_tQheHJ0a-P35M"  # tester bot
    fake_url = "https://fakeurl.com/telegram/bot"
    with unittest.mock.patch(
        "application.bot_telegram._get_access_token", return_value=access,
    ):
        with unittest.mock.patch(
            "application.bot_telegram._get_url", return_value=fake_url,
        ):
            with unittest.mock.patch.object(
                bot_telegram.BotAPI, "_bot_reply", return_value=None
            ):
                yield access


@pytest.fixture
def mock_token_inexistent():
    access = "0092916972:AAEvZGLAeZbpMzcuTLwdc_tQh35eHJ0a-P3"  # fake
    with unittest.mock.patch(
        "application.bot_telegram._get_access_token", return_value=access,
    ):
        yield access
