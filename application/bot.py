from environs import Env
from dotenv import load_dotenv
from dotenv import find_dotenv

import requests
import flask

from . import services

env = Env()
load_dotenv(find_dotenv())

FB_ACCESS_TOKEN = env("FB_ACCESS_TOKEN", None)
FB_VERIFY_TOKEN = env("FB_VERIFY_TOKEN", None)

app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def verify_token():
    if flask.request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
        return flask.request.args.get("hub.challenge")
    return flask.Response(response={'Wrong Verify Token'}, status=400)


def bot_reply(sender, message):
    payload = {
        "recipient": {"id": sender},
        "message": {"text": message},
    }

    requests.post(
        "https://graph.facebook.com/v2.6/me/messages/?access_token="
        + FB_ACCESS_TOKEN,
        json=payload,
    )


@app.route("/", methods=["POST"])
def bot():
    data = flask.request.json
    sender = data["entry"][0]["messaging"][0]["sender"]["id"]

    text = data["entry"][0]["messaging"][0]["message"]["text"]
    user_message = services.verify_user_input(text)
    if not isinstance(user_message, int):
        bot_reply(sender, user_message)
        return flask.Response(response=user_message, status=200)

    bot_reply(sender, "All is good for now!")
    return flask.Response(response='OK', status=200)


@app.route("/conversation", methods=["POST"])
def create_conversation():
    data = dict(flask.request.form)
    conversation = services.create_conversation(data)

    conversation.created_at = str(conversation.created_at)
    conversation.__dict__.pop("_sa_instance_state")

    response = app.response_class(
        response=flask.json.dumps(conversation.__dict__),
        status=201,
        mimetype="application/json",
    )
    return response


@app.route("/conversation", methods=["GET"])
def get_conversation():
    conversation = services.get_conversation_by_id(flask.request.values["id"])

    if not conversation:
        return flask.Response(response={}, status=404)

    conversation.created_at = str(conversation.created_at)
    conversation.__dict__.pop("_sa_instance_state")

    response = app.response_class(
        response=flask.json.dumps(conversation.__dict__),
        status=200,
        mimetype="application/json",
    )
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
