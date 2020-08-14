import flask
from flask import views

from . import services
from . import database


class ConversationAPI(views.MethodView):
    def _format_conversation(self, conversation):
        conversation.created_at = str(conversation.created_at)
        conversation.__dict__.pop("_sa_instance_state")
        return conversation.__dict__

    def get(self, conversation_id):
        conversation = None
        with database.get_db() as db:
            conversation = services.Conversation(db).get_conversation_by_id(
                conversation_id
            )

        if not conversation:
            return flask.Response(response={}, status=404)

        conversation = self._format_conversation(conversation)
        return conversation, 200
