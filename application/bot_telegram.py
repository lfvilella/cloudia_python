import flask
from flask import views

import telegram

from . import services
from . import database
from . import settings


def _get_url():
    return settings.URL


def _get_access_token():
    return settings.TELEGRAM_TOKEN


def _get_bot():
    return telegram.Bot(token=_get_access_token())


class BotAPI(views.MethodView):
    def __init__(self):
        self._bot = _get_bot()

    def _set_webhook(self, token):
        try:
            return self._bot.setWebhook(f"{_get_url()}{token}")
        except telegram.error.Unauthorized:
            return False

    def get(self, token=None):
        set_webhook = self._set_webhook(
            token or _get_access_token()
        )
        if not set_webhook:
            return flask.Response(
                response={"Webhook Setup Failed"}, status=400
            )
        return flask.Response(response={"Webhook Setup OK"}, status=200)

    def _bot_reply(self, chat_id, text, reply_to_message_id):
        reply = self._bot.sendMessage(
            chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id
        )
        return reply.to_json()

    def post(self, token=None):
        update = telegram.Update.de_json(
            flask.request.get_json(force=True), self._bot
        )  # JSON to Telegram object

        chat_id = update.message.chat.id
        message_id = update.message.message_id
        text = update.message.text.encode("utf-8").decode()

        user_message = services.Bot().verify_user_input(text)
        if not isinstance(user_message, int):
            self._bot_reply(
                chat_id=chat_id,
                text=user_message,
                reply_to_message_id=message_id,
            )
            return flask.Response(response=user_message, status=200)

        fizz_buzz = services.Bot().is_fizz_buzz(user_message)

        self._bot_reply(
            chat_id=chat_id, text=fizz_buzz, reply_to_message_id=message_id
        )

        # Saves conversation
        user_id = update.message.from_user.id
        with database.get_db() as db:
            services.Conversation(db).create_conversation(
                user_identifier=user_id, user_message=text, bot_reply=fizz_buzz
            )

        return flask.Response(response=fizz_buzz, status=200)
