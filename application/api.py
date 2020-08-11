import flask
from flask.views import MethodView

from . import services


app = flask.Flask(__name__)


class ConversationAPI(MethodView):
    def _format_conversation(self, conversation):
        conversation.created_at = str(conversation.created_at)
        conversation.__dict__.pop("_sa_instance_state")
        return conversation.__dict__

    def get(self, conversation_id):
        conversation = services.get_conversation_by_id(conversation_id)

        if not conversation:
            return flask.Response(response={}, status=404)

        conversation = self._format_conversation(conversation)

        response = app.response_class(
            response=flask.json.dumps(conversation),
            status=200,
            mimetype="application/json",
        )
        return response
