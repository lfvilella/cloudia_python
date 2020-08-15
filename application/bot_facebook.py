import flask
import flask.views

from . import services


_service = services.FacebookBot()


class BotAPI(flask.views.MethodView):
    def get(self):
        response = None
        try:
            response = _service.start_webhook(flask.request.args)
        except services.ServiceException as error:
            response = str(error)
        return response, 200

    def post(self):
        message = None
        try:
            message = _service.reply_message(flask.request.json)
        except services.ServiceException as error:
            message = str(error)
        return message, 200
