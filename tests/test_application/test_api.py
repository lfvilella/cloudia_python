import pytest

from application import app
from application import models


client = app.app.test_client()


@pytest.mark.usefixtures("use_db")
class TestConversation:
    @pytest.fixture
    def create_fake_conversation(self, session_maker):
        session = session_maker()

        conversation = models.Conversation(
            user_identifier="fakeuserid",
            user_message="Hello Bot!!!",
            bot_reply="The message must be an integer!",
        )

        session.add(conversation)
        session.flush()
        session.commit()
        return conversation

    def test_get_conversation(self, create_fake_conversation):
        conversation = create_fake_conversation
        response = client.get(f"/conversation/{conversation.id}")

        assert response.status_code == 200
        assert response.json == {
            "bot_reply": conversation.bot_reply,
            "created_at": str(conversation.created_at),
            "id": conversation.id,
            "user_message": conversation.user_message,
            "user_identifier": conversation.user_identifier,
        }

    def test_get_unexist_conversation(self):
        response = client.get("/conversation/fakeid")
        assert response.status_code == 404