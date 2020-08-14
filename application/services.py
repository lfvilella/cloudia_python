from . import models


class Conversation:
    def __init__(self, db):
        self._db = db

    def get_conversation_by_id(self, _id: str):
        return self._db.query(models.Conversation).get(_id)

    def create_conversation(
        self,
        user_identifier: str,
        user_message: str,
        bot_reply: str,
        persist: bool = True,
    ) -> models.Conversation:

        conversation = models.Conversation()
        conversation.user_identifier = user_identifier
        conversation.user_message = user_message
        conversation.bot_reply = bot_reply

        self._db.add(conversation)
        if persist:
            self._db.commit()

        self._db.flush()
        return conversation


class Bot:
    def verify_user_input(self, user_message: str):
        if len(user_message) > 280:
            return "The message cannot exceed 280 characters!"

        try:
            return int(user_message)
        except ValueError:
            return "The message must be an integer!"

    def is_fizz_buzz(self, number: int) -> str:
        buzz = "Buzz" if number % 5 == 0 else ""
        fizz = "Fizz" if number % 3 == 0 else ""
        return f"{fizz}{buzz}" or f"Number {number} is not fizzbuzz..."
