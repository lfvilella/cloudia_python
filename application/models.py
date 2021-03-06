import uuid
import datetime

import sqlalchemy
import sqlalchemy.orm

from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = sqlalchemy.Column(
        sqlalchemy.String(36),
        primary_key=True,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_identifier = sqlalchemy.Column(sqlalchemy.String(280))
    user_message = sqlalchemy.Column(sqlalchemy.String(280))
    bot_reply = sqlalchemy.Column(sqlalchemy.String(280))
    source = sqlalchemy.Column(sqlalchemy.String(20))
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.utcnow()
    )
