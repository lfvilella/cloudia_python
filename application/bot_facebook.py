import requests
import flask
from flask import views

from . import services
from . import database
from . import settings


def _get_verify_token():
    return settings.FB_VERIFY_TOKEN


def _get_access_token():
    return settings.FB_ACCESS_TOKEN


class BotAPI(views.MethodView):
    def get(self):
        """
        Verify Token
        """

        if flask.request.args.get("hub.verify_token") == _get_verify_token():
            return flask.request.args.get("hub.challenge")
        return flask.Response(response={"Wrong Verify Token"}, status=400)

    def _bot_reply(self, sender, message):
        payload = {
            "recipient": {"id": sender},
            "message": {"text": message},
        }
        response = requests.post(
            "https://graph.facebook.com/v2.6/me/messages/?access_token="
            + _get_access_token(),
            json=payload,
        )
        data = {
            "recipient_id": response.json()["recipient_id"],
            "message_id": response.json()["message_id"],
        }
        return data

    def post(self):
        """
        Facebook Bot
        """

        data = None
        try:
            data = flask.request.json
        except TypeError as error:
            return print(error)

        sender = data["entry"][0]["messaging"][0]["sender"]["id"]
        text = data["entry"][0]["messaging"][0]["message"]["text"]

        user_message = services.Bot().verify_user_input(text)
        if not isinstance(user_message, int):
            self._bot_reply(sender, user_message)
            return flask.Response(response=user_message, status=200)

        fizz_buzz = services.Bot().is_fizz_buzz(user_message)
        self._bot_reply(sender, fizz_buzz)

        # Saves conversation
        with database.get_db() as db:
            services.Conversation(db).create_conversation(
                user_identifier=sender, user_message=text, bot_reply=fizz_buzz
            )

        return flask.Response(response=fizz_buzz, status=200)
