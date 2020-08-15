import pytest

from application import app
from application import models


client = app.app.test_client()


@pytest.mark.usefixtures("use_db")
class TestConversation:
    @pytest.fixture
    def create_fake_conversation(self, session_maker):
        def create():
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

        return create

    def test_list_conversations(self, create_fake_conversation):
        conversation1 = create_fake_conversation()
        conversation2 = create_fake_conversation()
        response = client.get("/conversations")

        assert response.status_code == 200
        assert response.json == {
            "data": [
                {
                    "bot_reply": conversation1.bot_reply,
                    "created_at": str(conversation1.created_at),
                    "id": conversation1.id,
                    "source": None,
                    "user_identifier": conversation1.user_identifier,
                    "user_message": conversation1.user_message,
                },
                {
                    "bot_reply": conversation2.bot_reply,
                    "created_at": str(conversation2.created_at),
                    "id": conversation2.id,
                    "source": None,
                    "user_identifier": conversation2.user_identifier,
                    "user_message": conversation2.user_message,
                },
            ]
        }
