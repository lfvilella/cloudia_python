import flask
import flask.views

from . import services


_service = services.TelegramBot()


class BotAPI(flask.views.MethodView):
    def get(self):
        return "working", 200

    def post(self):
        message = None
        try:
            message = _service.reply_message(flask.request.json)
        except services.ServiceException as error:
            message = str(error)
        return message, 200
