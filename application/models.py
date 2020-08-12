import uuid
import datetime

import sqlalchemy
import sqlalchemy.orm

from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = sqlalchemy.Column(
        sqlalchemy.String,
        primary_key=True,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    username = sqlalchemy.Column(sqlalchemy.String)
    user_message = sqlalchemy.Column(sqlalchemy.String)
    bot_reply = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.utcnow()
    )
