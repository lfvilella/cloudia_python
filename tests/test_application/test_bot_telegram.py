import pytest

from application import app
from application import models


client = app.app.test_client()

_URL = "/telegram/bot"


@pytest.mark.usefixtures("mock_bot_telegram", "use_db")
class TestTelegramBot:
    def payload(self, message):
        return {
            "update_id": 123456789,
            "message": {
                "message_id": 123,
                "from": {
                    "id": 1234567890,
                    "is_bot": False,
                    "first_name": "Fake Name",
                    "last_name": "LastName",
                    "language_code": "pt-br",
                },
                "chat": {
                    "id": 1234567890,
                    "first_name": "Fake Name",
                    "last_name": "LastName",
                    "type": "private",
                    "default_quote": None,
                    "photo": None,
                    "pinned_message": None,
                    "permissions": None,
                },
                "date": 1597374715,
                "text": str(message),
                "default_quote": None,
            },
        }

    def test_saves_conversation_on_db(self, session_maker):
        assert session_maker().query(models.Conversation).count() == 0
        payload = self.payload("3")
        client.post(_URL, json=payload)
        assert session_maker().query(models.Conversation).count() == 1

    def test_bot_reply_saves_on_db(self, session_maker):
        user_message = "3"
        payload = self.payload(user_message)
        response = client.post(_URL, json=payload)

        db_conversation = session_maker().query(models.Conversation).first()
        assert db_conversation.bot_reply == response.data.decode()
        assert db_conversation.user_message == user_message

    def test_invalid_input_dont_saves_on_db(self, session_maker):
        assert session_maker().query(models.Conversation).count() == 0
        payload = self.payload("Hi Robot!!!")
        client.post(_URL, json=payload)
        assert session_maker().query(models.Conversation).count() == 0

    def test_bot_with_string_input(self):
        payload = self.payload("Hi Bot!!")
        response = client.post(_URL, json=payload)
        assert response.data.decode() == "The message must be an integer!"

    def test_bot_with_not_fizz_buzz_input(self):
        payload = self.payload("1")
        response = client.post(_URL, json=payload)
        assert response.data.decode() == "Number 1 is not fizzbuzz..."

    def test_bot_with_fizz_input(self):
        payload = self.payload("3")
        response = client.post(_URL, json=payload)
        assert response.data.decode() == "Fizz"

    def test_bot_with_buzz_input(self):
        payload = self.payload("5")
        response = client.post(_URL, json=payload)
        assert response.data.decode() == "Buzz"

    def test_bot_with_fizz_buzz_input(self):
        payload = self.payload("15")
        response = client.post(_URL, json=payload)
        assert response.data.decode() == "FizzBuzz"

    def test_bot_with_size_gt_280(self):
        payload = self.payload(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do"
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
            "enim ad minim veniam, quis nostrud exercitation ullamco laboris "
            "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor "
            "in reprehenderit in voluptate velit esse cillum dolore eu fugiat"
            " nulla pariatur. Excepteur sint occaecat cupidatat non proident,"
            " sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
        response = client.post(_URL, json=payload)
        assert (
            response.data.decode()
            == "The message cannot exceed 280 characters!"
        )
