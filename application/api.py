from flask import views

from . import services
from . import database


class ConversationAPI(views.MethodView):
    def _format_conversation(self, conversation):
        conversation.created_at = str(conversation.created_at)
        conversation.__dict__.pop("_sa_instance_state")
        return conversation.__dict__

    def get(self):
        conversations = []
        with database.get_db() as db:
            conversations = [
                self._format_conversation(c)
                for c in services.Conversation(db).get_conversations()
            ]
        return {"data": conversations}, 200
