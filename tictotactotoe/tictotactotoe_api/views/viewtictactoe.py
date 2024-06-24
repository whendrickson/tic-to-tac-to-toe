from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .base import TicToTacToToeAPIView
from ..tictactoe import game_get, game_post, get_moves, games_get, games_post, game_put
from ..serializers import GameSerializer, MoveSerializer
from ..models import Moves as MovesModel
import sys
import traceback


class GameView(TicToTacToToeAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = GameSerializer

    @extend_schema(operation_id="v1_game_retrieve")
    def get(self, request, **kwargs):
        self.log.debug("Look at someone getting this single game!")
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
        self.log.debug(f"User {request.user.username} wants the seat!")
        response_code = status.HTTP_400_BAD_REQUEST
        status_message, message, data = game_put(kwargs.get("game_id"), request.user.id, request.data)
        if status_message == "ok":
            response_code = status.HTTP_202_ACCEPTED
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )


class GamesView(TicToTacToToeAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GameSerializer

    @extend_schema(operation_id="v1_games_retrieve")
    def get(self, request, **kwargs):
        self.log.debug("Look at someone getting the games!")
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
    permission_classes = (IsAuthenticated,)
    serializer_class = MoveSerializer

    def get(self, request, **kwargs):
        queryset = MovesModel.objects.filter(game__id=kwargs.get("game_id"))
        serializer = MoveSerializer(queryset, many=True)
        return self._response(
            data=serializer.data,
            response_code=status.HTTP_200_OK,
            message="ok",
            status_message="Here are the moves!",
        )

    def post(self, request, **kwargs):
        username = request.user.username
        self.log.debug(f"User {username} is making a move!")
        response_code = status.HTTP_400_BAD_REQUEST
        status_message = "error"
        data = {}
        # todo: this wrapping needs to happen everywhere!
        try:
            status_message, message, data = game_post(kwargs.get("game_id"), username, request.data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error!"
            self.log.error(
                f"{exc_type.__name__}: {e}",
                extra={
                    "ExceptionType": exc_type.__name__,
                    "LineNumber": exc_tb.tb_lineno,
                    "Message": str(e),
                    "FullTraceback": str(traceback.format_exc()),
                }
            )
        if status_message == "ok":
            response_code = status.HTTP_201_CREATED
        return self._response(
            data=data,
            response_code=response_code,
            message=message,
            status_message=status_message,
        )

