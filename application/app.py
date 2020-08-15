import flask

from . import models
from . import database
from . import api
from . import bot_facebook
from . import bot_telegram


# Create DB
models.Base.metadata.create_all(bind=database.get_engine())


app = flask.Flask(__name__)


app.add_url_rule(
    "/facebook/bot", view_func=bot_facebook.BotAPI.as_view("facebook_bot")
)

app.add_url_rule(
    "/telegram/bot", view_func=bot_telegram.BotAPI.as_view("telegram_bot")
)

app.add_url_rule(
    "/conversations", view_func=api.ConversationAPI.as_view("conversations"),
)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
