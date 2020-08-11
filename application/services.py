from . import models, database


class ServicesException(Exception):
    """ Services Exception
    This error is raised when data passed to the function is not valid
    """

    pass


class ValidationError(ServicesException):
    pass


# Create DB
models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        return db
    finally:
        db.close()


def get_conversation_by_id(_id: str):
    db = get_db()
    return db.query(models.Conversation).get(_id)


def create_conversation(
    data: dict, persist: bool = True
) -> models.Conversation:
    db = get_db()

    conversation = models.Conversation()
    conversation.username = data["username"]
    conversation.user_message = data["user_message"]
    conversation.bot_reply = data["bot_reply"]

    db.add(conversation)
    if persist:
        db.commit()

    db.flush()
    return conversation


def verify_user_input(user_message):
    if len(user_message) > 280:
        return "The message cannot exceed 280 characters!"

    try:
        return int(user_message)
    except ValueError:
        return "The message must be an integer!"
