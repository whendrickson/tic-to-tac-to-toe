"""
Copyright 2024 Wes Hendrickson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


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
                "message": message,
            },
            status=response_code,
        )
