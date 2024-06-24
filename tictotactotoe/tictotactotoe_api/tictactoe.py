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

from django.contrib.auth.models import User as UserModel
from .models import Games as GamesModel
from .models import Moves as MovesModel
from .serializers import GameSerializer, MoveSerializer


def _all_same(items: list) -> bool:
    """
    See if all the items in a list are the same.

    :param items: Random list of items.
    :type items: list.
    :return: Boolean.
    :rtype: bool
    """
    return len(set(items)) == 1


def _check_diagonal(moves: list):
    """
    Check to see if the moves in the game have a winning diagonal line.

    :param moves: All moves in the game.
    :type moves: list.
    :return: Either the winning or None
    :rtype: str or None.
    """

    n = len(moves)
    line = []
    for i in range(n):
        line.append(moves[i][i])
    if _all_same(line):
        return line[0]
    line = []
    k = n - 1
    for i in range(n):
        line.append(moves[i][k])
        k -= 1
    if _all_same(line):
        return line[0]
    return None


def _check_full(moves: list) -> bool:
    """
    Check to see if the moves in the game have been played.

    :param moves: All moves in the game.
    :type moves: list.
    :return: Boolean.
    :rtype: bool.
    """
    for e in moves:
        fix = e.index(None) if None in e else None
        if fix is not None:
            return False
    return True


def _check_horizontal(moves: list):
    """
    Check to see if the moves in the game have a winning horizontal line.

    :param moves: All moves in the game.
    :type moves: list.
    :return: Either the winning or None
    :rtype: str or None.
    """
    for i in moves:
        if i[0] is not None and _all_same(i):
            return i[0]


def _check_vertical(moves: list):
    """
    Check to see if the moves in the game have a winning vertical line.

    :param moves: All moves in the game.
    :type moves: list.
    :return: Either the winning or None
    :rtype: str or None.
    """
    max_x = 3
    max_y = 3
    for x in range(0, max_x):
        line = []
        for y in range(0, max_y):
            line.append(moves[y][x])
        if line[0] is not None and _all_same(line):
            return line[0]
    return None


def game_get(game_id: str) -> dict:
    """
    Based on the game ID get it from the database.

    :param game_id: The ID that has been assigned to the game.
    :type game_id: str.
    :return: Game details.
    :rtype: dict.
    """
    try:
        game = GamesModel.objects.get(id=game_id)
        serializer = GameSerializer(game, many=False)
        return serializer.data
    except GamesModel.DoesNotExist:
        return {}
    except Exception:
        # this is not practice but will not boil the ocean currently
        return {}


def game_post(game_id: str, username: str, data: dict):
    """
    A player is making a move on the board.

    :param game_id: The ID that has been assigned to the game.
    :type game_id: str.
    :param username: API Request username.
    :type username: str.
    :param data: Django request data.
    :type data: dict.
    :return: status_message, message, data
    :rtype: str, str, dict
    """

    game = GamesModel.objects.get(id=game_id)

    player = None
    players = []
    for i in ["x", "o"]:
        players.append(str(getattr(game, f"player_{i}")))
        if str(username) == str(getattr(game, f"player_{i}")):
            player = i

    if str(None) in players:
        return "error", "Not all players are ready. Please wait!", {}

    if player is None:
        return "error", f"Sorry {username} is not apart of this game!", {}

    serializer = MoveSerializer(data={
        "x": data.get("x"),
        "y": data.get("y"),
        "player": player,
    })
    if not serializer.is_valid():
        # todo: make serializer.errors pretty!
        return "error", str(serializer.errors), {}

    x = serializer.validated_data.get("x")
    y = serializer.validated_data.get("y")

    # check to see if the game is over or tied.
    game_state = getattr(game, "state")
    if not game_state.startswith("turn_"):
        if game_state == "winner_x":
            return "error", f"Game is over! Player X is the winner!", {}
        if game_state == "winner_y":
            return "error", f"Game is over! Player Y is the winner!", {}
        return "error", f"Game is over! Ended in Tie!", {}

    if not valid_move(x, y):
        return "error", "Move was not valid. Please try a different move!", {}

    other_player = "x"
    if player == "x":
        other_player = "o"
    if f"turn_{player}" != getattr(game, "state"):
        return "error", f"It is not your turn {player}! Sorry, please wait for {other_player}.", {}

    previous_move = MovesModel.objects.filter(
        game=game,
        x=serializer.validated_data.get("x"),
        y=serializer.validated_data.get("y"),
    )
    if previous_move:
        return "error", "I am sorry a player already placed a move here!", {}
    serializer.save(game=game)

    winner = get_winner(game_id)
    if winner is None:
        message = f"Move accepted! Now it is {other_player}'s turn."
        setattr(game, "state", f"turn_{other_player}")
    elif winner in ["x", "o"]:
        message = f"Congratulations {player} you are the winner!"
        setattr(game, "state", f"winner_{player}")
    elif winner == "tie":
        message = "Full board! Game ended in a tie."
        setattr(game, "state", "tie")
    else:
        return "error", f"Something went wrong! {winner}", {}
    game.save()
    return "ok", message, serializer.data


def games_get():
    """
    Get all the games in the database.

    :return: status_message, message, data
    :rtype: str, str, dict
    """
    # todo: setup filters and limits
    games = GamesModel.objects.all()
    serializer = GameSerializer(games, many=True)
    return "ok", "Here are the games!", serializer.data


def games_post(data: dict):
    """
    Create a game match.

    :param data: Django request data.
    :type data: dict.
    :return: status_message, message, data
    :rtype: str, str, dict
    """
    serializer = GameSerializer(data=data)
    if not serializer.is_valid():
        # todo: make serializer.errors pretty!
        return "error", str(serializer.errors), {}
    serializer.save()
    return "ok", "Game was created!", serializer.data


def game_put(game_id, user_id, data):
    game = GamesModel.objects.get(id=game_id)
    user = UserModel.objects.get(id=user_id)

    symbol = data.get("player")
    if getattr(game, f"player_{symbol}") is not None:
        return "error", f"Someone is already {symbol}", {}
    setattr(game, f"player_{symbol}", user)

    players = []
    for i in ["player_x", "player_o"]:
        players.append(str(getattr(game, i)))

    if len(list(set(players))) != 2:
        return "error", "Cannot be the same user for both players!", {}
    # todo: send back the game as data! this a nice to have!
    game.save()
    return "ok", f"Set as player {symbol}", {}


def get_moves(game_id: str) -> list:
    """
    Gather all the moves in the game performed or not.

    :param game_id: The ID that has been assigned to the game.
    :type game_id: str.
    :return: A list of all the moves in the game.
    :rtype: list.
    """

    game = GamesModel.objects.get(id=game_id)
    moves_object = MovesModel.objects.filter(game=game)
    moves_serializer = MoveSerializer(moves_object, many=True)

    moves = [[None] * 3 for _ in range(3)]
    for move in moves_serializer.data:
        moves[move["y"]][move["x"]] = move["player"]
    return moves


def get_winner(game_id: str) -> str:
    """
    Determine if there is a winner in the match based on moves.

    :param game_id: The ID that has been assigned to the game.
    :type game_id: str.
    :return: The winning player, tie or None if the matches is still playing.
    :rtype: str.
    """
    moves = get_moves(game_id)

    horizontal = _check_horizontal(moves)
    if horizontal is not None:
        return horizontal
    vertical = _check_vertical(moves)
    if vertical is not None:
        return vertical
    diagonal = _check_diagonal(moves)
    if diagonal is not None:
        return diagonal
    if _check_full(moves):
        return "tie"


def valid_move(x: int, y: int) -> bool:
    """

    :param x:
    :param y:
    :return:
    """
    min_x = 0
    max_x = 2  # think about maybe making this dynamic?
    min_y = 0
    max_y = 2  # think about maybe making this dynamic?

    if x < min_x or x > max_x:
        return False
    if y < min_y or y > max_y:
        return False
    return True
