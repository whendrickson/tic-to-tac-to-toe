from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import logging


class TicToTacToToeAPIView(GenericAPIView):
    """
    This is a super basic class to set the parser classes and the default logger.
    """
    parser_classes = [JSONParser]

    def __init__(self):
        self.log = logging.getLogger("api")
        super().__init__()

    @staticmethod
    def _response(response_code, data=None, message="", status_message="ok"):
        if data is None:
            data = {}
        return Response(
            data={
                "data": data,
                "status": status_message,
                "message": message
            },
            status=response_code,
        )
