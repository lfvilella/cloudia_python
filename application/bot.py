import os
import json

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


@app.route("/", methods=["GET", "POST"])
def webhook():
    if flask.request.method == "POST":
        try:
            data = json.loads(flask.request.data.decode())
            text = data["entry"][0]["messaging"][0]["message"]["text"]
            len_text = len(text)
            sender = data["entry"][0]["messaging"][0]["sender"]["id"]
            payload = {
                "recipient": {"id": sender},
                "message": {"text": f"Your input have {len_text} letters."},
            }
            requests.post(
                "https://graph.facebook.com/v2.6/me/messages/?access_token="
                + FB_ACCESS_TOKEN,
                json=payload,
            )
        except Exception as error:
            print(error)

    if flask.request.method == "GET":
        if flask.request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return flask.request.args.get("hub.challenge")
        return "Wrong Verify Token"

    return "Nothing"


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
