import flask

from . import api
from . import bot_facebook


app = flask.Flask(__name__)

app.add_url_rule("/bot", view_func=bot_facebook.BotAPI.as_view("bot"))
app.add_url_rule(
    "/conversation", view_func=api.ConversationAPI.as_view("conversation")
)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
