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

import sys
import traceback
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .base import TicToTacToToeAPIView
from ..tictactoe import game_get, game_post, get_moves, games_get, games_post, game_put
from ..serializers import GameSerializer, MoveSerializer
from ..models import Moves as MovesModel


class GameView(TicToTacToToeAPIView):
    """
    Specific Tic-Tac-Toe game.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = GameSerializer

    @extend_schema(operation_id="v1_game_retrieve")
    def get(self, request, **kwargs):
        """
        Game details.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        self.log.debug("Look at %s getting this single game!", request.user.username)
        message = "Game not found!"
        status_message = "error"
        response_code = status.HTTP_404_NOT_FOUND
        game_id = kwargs.get("game_id")

        data = game_get(game_id)
        if data:
            message = "Look at this awesome game!"
            status_message = "ok"
            response_code = status.HTTP_200_OK
            data["moves"] = get_moves(game_id)
        return self._response(
            data=data,
            message=message,
            response_code=response_code,
            status_message=status_message,
        )

    def put(self, request, **kwargs):
        """
        Update game.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        self.log.debug("User %s wants the seat!", request.user.username)
        response_code = status.HTTP_400_BAD_REQUEST
        status_message, message, data = game_put(
            kwargs.get("game_id"),
            request.user.id,
            request.data,
        )
        if status_message == "ok":
            response_code = status.HTTP_202_ACCEPTED
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )


class GamesView(TicToTacToToeAPIView):
    """
    List all the Tic-Tac-Toe games.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = GameSerializer

    @extend_schema(operation_id="v1_games_retrieve")
    def get(self, request, **kwargs):
        """
        Multiple game details.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        self.log.debug("Look at %s getting the games!", request.user.username)
        response_code = status.HTTP_400_BAD_REQUEST
        status_message, message, data = games_get()
        if status_message == "ok":
            response_code = status.HTTP_200_OK
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )

    def post(self, request, **kwargs):
        """
        Create a game.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        self.log.debug("New game was received.")
        response_code = status.HTTP_400_BAD_REQUEST
        status_message, message, data = games_post(request.data)
        if status_message == "ok":
            response_code = status.HTTP_201_CREATED
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )


class MovesView(TicToTacToToeAPIView):
    """
    Moves for a specific Tic-Tac-Toe game.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MoveSerializer

    def get(self, request, **kwargs):
        """
        Gather moves for a specific game.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        self.log.debug("Look at %s wants the moves!", request.user.username)
        queryset = MovesModel.objects.filter(game__id=kwargs.get("game_id"))
        serializer = MoveSerializer(queryset, many=True)
        return self._response(
            data=serializer.data,
            response_code=status.HTTP_200_OK,
            message="ok",
            status_message="Here are the moves!",
        )

    def post(self, request, **kwargs):
        """
        Making a moving on a specific game.

        :param request: Django request object.
        :param kwargs: Keyword arguments.
        :return: Api Response.
        """

        username = request.user.username
        self.log.debug("User %s is making a move!", username)
        response_code = status.HTTP_400_BAD_REQUEST
        status_message = "error"
        data = {}
        # todo: this wrapping needs to happen everywhere!
        try:
            status_message, message, data = game_post(
                kwargs.get("game_id"),
                username,
                request.data,
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error!"
            log_error_message = f"{exc_type.__name__}: {e}"
            self.log.error(
                log_error_message,
                extra={
                    "ExceptionType": exc_type.__name__,
                    "LineNumber": exc_tb.tb_lineno,
                    "Message": str(e),
                    "FullTraceback": str(traceback.format_exc()),
                },
            )
        if status_message == "ok":
            response_code = status.HTTP_201_CREATED
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )
