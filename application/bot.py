import flask

from . import services


app = flask.Flask(__name__)


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
