import flask
import flask.views

from . import services


_service = None


def _get_service():
    global _service
    if _service:
        return _service
    _service = services.FacebookBot()
    return _service


class BotAPI(flask.views.MethodView):
    def get(self):
        response = None
        try:
            response = _get_service().start_webhook(flask.request.args)
        except services.ServiceException as error:
            response = str(error)
            return response, 400
        return response, 200

    def post(self):
        message = None
        try:
            message = _get_service().reply_message(flask.request.json)
        except services.ServiceException as error:
            message = str(error)
            return message, 400
        return message, 200
