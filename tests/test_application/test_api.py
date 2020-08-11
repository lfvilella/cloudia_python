import pytest

from application import urls
from application import models


client = urls.app.test_client()


@pytest.mark.usefixtures("use_db")
class TestConversation:
    @pytest.fixture
    def payload_data(self):
        return {
            "username": "fakeusername",
            "user_message": "Hello Bot!!!",
            "bot_reply": "Sorry, I only accept integer numbers.",
        }

    def test_create_conversation_returns_201(self, payload_data):
        response = client.post("/conversation", data=payload_data)
        response.json.pop("id")
        response.json.pop("created_at")

        assert response.status_code == 201
        assert response.json == payload_data

    def test_create_conversation_saves_on_db(
        self, session_maker, payload_data
    ):
        assert session_maker().query(models.Conversation).count() == 0
        response = client.post("/conversation", data=payload_data)
        assert session_maker().query(models.Conversation).count() == 1

        db_conversation = session_maker().query(models.Conversation).first()
        db_conversation.created_at = str(db_conversation.created_at)
        db_conversation.__dict__.pop("_sa_instance_state")
        assert db_conversation.__dict__ == response.json

    def test_get_conversation(self, payload_data):
        conversation = client.post("/conversation", data=payload_data)
        _id = conversation.json["id"]

        response = client.get(f"/conversation?id={_id}")

        assert response.status_code == 200

        payload_data["id"] = _id
        payload_data["created_at"] = conversation.json["created_at"]
        assert response.json == payload_data

    def test_get_unexist_conversation(self, payload_data):
        response = client.get("/conversation?id=fakeid")
        assert response.status_code == 404
