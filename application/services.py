import abc

import requests

from . import database
from . import models
from . import settings


class ServiceException(Exception):
    pass


class ValidationError(ServiceException):
    pass


class ReplyError(ServiceException):
    pass


class Conversation:
    def __init__(self, db):
        self._db = db

    def get_conversations(self):
        return self._db.query(models.Conversation).all()

    def get_conversation_by_id(self, _id: str):
        return self._db.query(models.Conversation).get(_id)

    def create_conversation(
        self,
        user_identifier: str,
        user_message: str,
        bot_reply: str,
        source: str,
        persist: bool = True,
    ) -> models.Conversation:

        conversation = models.Conversation()
        conversation.user_identifier = user_identifier
        conversation.user_message = user_message
        conversation.bot_reply = bot_reply
        conversation.source = source

        self._db.add(conversation)
        if persist:
            self._db.commit()

        self._db.flush()
        return conversation


class ServiceBot(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def _bot_reply(self, bot_reply_message, message_data):
        pass

    @abc.abstractclassmethod
    def _get_user_message(self, message_data) -> str:
        pass

    @abc.abstractclassmethod
    def _get_user_identifier(self, message_data) -> str:
        pass

    @abc.abstractclassmethod
    def _get_source_website(self) -> str:
        pass

    def _save_on_db(
        self, user_identifier: str, user_message: str, bot_reply: str
    ):
        with database.get_db() as db:
            Conversation(db).create_conversation(
                user_identifier=user_identifier,
                user_message=user_message,
                bot_reply=bot_reply,
                source=self._get_source_website(),
            )

    def verify_user_input(self, user_message: str):
        if len(user_message) > 280:
            raise ValidationError("The message cannot exceed 280 characters!")

        try:
            return int(user_message)
        except ValueError:
            raise ValidationError("The message must be an integer!")

    def get_fizz_buzz_message(self, number: int) -> str:
        buzz = "Buzz" if number % 5 == 0 else ""
        fizz = "Fizz" if number % 3 == 0 else ""
        return f"{fizz}{buzz}" or f"Number {number} is not fizzbuzz..."

    def reply_message(self, message_data: dict):
        try:
            user_message = self._get_user_message(message_data)
            message = self.verify_user_input(user_message)
            bot_reply_message = self.get_fizz_buzz_message(message)
            self._bot_reply(bot_reply_message, message_data)
            self._save_on_db(
                user_identifier=self._get_user_identifier(message_data),
                user_message=user_message,
                bot_reply=bot_reply_message,
            )
            return bot_reply_message
        except ValidationError as error:
            self._bot_reply(str(error), message_data)
            raise


class TelegramBot(ServiceBot):
    _bot_api_url = "https://api.telegram.org/bot"
    _base_url = None
    _webhook_started = False

    def __init__(self):
        self._base_url = f"{self._bot_api_url}{self._get_access_token()}"
        self._start_webhook()

    def _get_local_bot_endpoint(self):
        return settings.TELEGRAM_URL

    def _get_access_token(self):
        return settings.TELEGRAM_TOKEN

    def _start_webhook(self, tries=0):
        if self._webhook_started:
            return

        self._webhook_started = True

        url = f"{self._base_url}/setWebhook"
        data = {"url": self._get_local_bot_endpoint()}

        response = requests.post(url, json=data)
        if not response.ok or not response.json()["ok"]:
            raise ServiceException("Unable to set hook")

    def _bot_reply(self, bot_reply_message, message_data):
        url = f"{self._base_url}/sendMessage"

        data = {
            "chat_id": message_data["message"]["chat"]["id"],
            "reply_to_message_id": message_data["message"]["message_id"],
            "text": bot_reply_message,
        }
        response = requests.post(url, json=data)
        if not response.ok or not response.json()["ok"]:
            raise ReplyError()

    def _get_user_message(self, message_data) -> str:
        return message_data["message"]["text"]

    def _get_user_identifier(self, message_data) -> str:
        return message_data["message"]["from"]["id"]

    def _get_source_website(self) -> str:
        return "telegram"


class FacebookBot(ServiceBot):
    def _get_verify_token(self):
        return settings.FB_VERIFY_TOKEN

    def _get_access_token(self):
        return settings.FB_ACCESS_TOKEN

    def start_webhook(self, params):
        hub_verify_token = params.get("hub.verify_token")
        if not hub_verify_token == self._get_verify_token():
            raise ServiceException("Wrong Verify Token")
        return params.get("hub.challenge")

    def _bot_reply(self, bot_reply_message, message_data):
        url = "https://graph.facebook.com/v2.6/me/messages/?access_token="
        payload = {
            "recipient": {"id": self._get_user_identifier(message_data)},
            "message": {"text": bot_reply_message},
        }

        response = requests.post(url + self._get_access_token(), json=payload)
        if not response.ok:
            raise ReplyError()

    def _get_user_message(self, message_data) -> str:
        return message_data["entry"][0]["messaging"][0]["message"]["text"]

    def _get_user_identifier(self, message_data) -> str:
        return message_data["entry"][0]["messaging"][0]["sender"]["id"]

    def _get_source_website(self) -> str:
        return "facebook"
