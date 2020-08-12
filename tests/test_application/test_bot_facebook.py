import urllib.parse

import pytest

from application import app
from application import models


client = app.app.test_client()


@pytest.mark.usefixtures("mock_bot_facebook", "use_db")
class TestBot:
    def payload(self, message):
        return {
            "object": "page",
            "entry": [
                {
                    "id": "fakeID",
                    "time": "1597171245694",
                    "messaging": [
                        {
                            "sender": {"id": "fakeSender"},
                            "recipient": {"id": "fakeID"},
                            "timestamp": "1597171245471",
                            "message": {
                                "mid": "whatever",
                                "text": str(message),
                            },
                        }
                    ],
                }
            ],
        }

    def test_verify_valid_token(self, mock_bot_facebook):
        query_string = urllib.parse.urlencode(
            {
                "hub.verify_token": mock_bot_facebook["verify"],
                "hub.challenge": "2067462119",
            }
        )

        response = client.get(f"/bot?{query_string}")
        assert response.status_code == 200

    def test_verify_invalid_token(self):
        response = client.get("/bot")
        assert response.status_code == 400

    def test_saves_conversation_on_db(self, session_maker):
        assert session_maker().query(models.Conversation).count() == 0
        payload = self.payload("3")
        client.post("/bot", json=payload)
        assert session_maker().query(models.Conversation).count() == 1

    def test_bot_reply_saves_on_db(self, session_maker):
        payload = self.payload("3")
        response = client.post("/bot", json=payload)

        db_conversation = session_maker().query(models.Conversation).first()
        assert db_conversation.bot_reply == response.data.decode()

    def test_invalid_input_dont_saves_on_db(self, session_maker):
        assert session_maker().query(models.Conversation).count() == 0
        payload = self.payload("Hi Robot!!!")
        client.post("/bot", json=payload)
        assert session_maker().query(models.Conversation).count() == 0

    def test_bot_with_string_input(self):
        payload = self.payload("Hi Bot!!")
        response = client.post("/bot", json=payload)
        assert response.data.decode() == "The message must be an integer!"

    def test_bot_with_fizz_input(self):
        payload = self.payload("3")
        response = client.post("/bot", json=payload)
        assert response.data.decode() == "Fizz"

    def test_bot_with_buzz_input(self):
        payload = self.payload("5")
        response = client.post("/bot", json=payload)
        assert response.data.decode() == "Buzz"

    def test_bot_with_fizz_buzz_input(self):
        payload = self.payload("15")
        response = client.post("/bot", json=payload)
        assert response.data.decode() == "Fizz-Buzz"

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
        response = client.post("/bot", json=payload)
        assert (
            response.data.decode()
            == "The message cannot exceed 280 characters!"
        )
