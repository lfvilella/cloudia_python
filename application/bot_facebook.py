from environs import Env
from dotenv import load_dotenv
from dotenv import find_dotenv

import requests
import flask
from flask.views import MethodView

from . import services


env = Env()
load_dotenv(find_dotenv())

FB_ACCESS_TOKEN = env("FB_ACCESS_TOKEN", None)
FB_VERIFY_TOKEN = env("FB_VERIFY_TOKEN", None)


class BotAPI(MethodView):
    def get(self):
        """
        Verify Token
        """

        if flask.request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return flask.request.args.get("hub.challenge")
        return flask.Response(response={"Wrong Verify Token"}, status=400)

    def _bot_reply(self, sender, message):
        payload = {
            "recipient": {"id": sender},
            "message": {"text": message},
        }
        requests.post(
            "https://graph.facebook.com/v2.6/me/messages/?access_token="
            + FB_ACCESS_TOKEN,
            json=payload,
        )

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

        user_message = services.verify_user_input(text)
        if not isinstance(user_message, int):
            self._bot_reply(sender, user_message)
            return flask.Response(response=user_message, status=200)

        fizz_buzz = services.is_fizz_buzz(user_message)
        self._bot_reply(sender, fizz_buzz)
        return flask.Response(response=fizz_buzz, status=200)
