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

from uuid import UUID, uuid4
import json
import random
import string
from django.test import TestCase


class TicToTacToToeApiTestCase(TestCase):
    """
    Let's play some Tie-Tac-Toe via the API to make sure it works!
    """

    def setUp(self):
        """
        Build the users data for playing the testing game.
        """

        user_x_password = self._password_generator(64)
        user_o_password = self._password_generator(64)
        user_z_password = self._password_generator(64)
        self.users = {
            "x": {
                "username": "test001",
                "password": user_x_password,
                "password2": user_x_password,
                "email": "email001@email.com",
                "first_name": "first001",
                "last_name": "last001",
            },
            "o": {
                "username": "test002",
                "password": user_o_password,
                "password2": user_o_password,
                "email": "email002@email.com",
                "first_name": "first002",
                "last_name": "last002",
            },
            "z": {
                "username": "test003",
                "password": user_z_password,
                "password2": user_z_password,
                "email": "email003@email.com",
                "first_name": "first003",
                "last_name": "last003",
            },
        }

    def tearDown(self):
        """
        Anything that would need to be ripped away after each test goes here.
        """

    def test_true(self):
        """
        Simple test to make sure things are true.
        """
        test = True
        self.assertTrue(test, True)

    def _client(self, method, uri, **kwargs):
        if not uri.startswith("/api"):
            uri = f"/api{uri}"
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
        return getattr(self.client, method)(
            uri,
            content_type="application/json",
            **kwargs,
        )

    def _game_get(self, game_id: str):
        """
        Gather game details.

        :param game_id: The ID of the game to be played.
        :return: Api response for the game.
        """
        return self._client("get", f"/v1/games/{game_id}")

    def _game_put(self, game_id: str, player: str):
        """
        Seat a player at the game.

        :param game_id: The ID of the game to be played.
        :type: str.
        :param player: The symbol to be played as during the game.
        :return: Api response for updating a game.
        """

        return self._client(
            "put",
            f"/v1/games/{game_id}",
            data={
                "player": player,
            },
        )

    def _games_post(self) -> str:
        """
        Create a game

        :return: Game id.
        """

        # typically we just want the game id so send it back
        game = self._client(
            "post",
            "/v1/games",
            data={
                "name": "test001",
            },
        )
        return game.json()["data"]["id"]

    def _login(self, player: str):
        """
        Login as a given player.

        :param player: The symbol for the player.
        :type player: str.
        :return: Api login response.
        """

        data = {
            "username": self.users[player].get("username"),
            "password": self.users[player].get("password"),
        }
        return self._client("post", "/v1/login", data=data)

    def _logout(self):
        """
        Sign out of the app.

        :return: Api logout response.
        """

        return self._client("post", "/v1/logout", data={})

    @staticmethod
    def _password_generator(length: int):
        """
        Generate a password based on a given length.

        :param length: How long the password should be.
        :type length: int.
        :return: Password.
        """

        choices = string.ascii_letters + string.digits + "!@#$%^&*()"
        return "".join(random.SystemRandom().choice(choices) for _ in range(length))

    def _play_game(self, moves: list):
        """
        Play a tic-tac-toe game back on a list of moves given.

        :param moves: Moves to be played.
        :type moves: list.
        :return: State of the last move.
        """
        self._setup_players()
        self._login("x")
        game_id = self._games_post()
        self._logout()
        for player in ["x", "o"]:
            self._login(player)
            self._game_put(game_id, player)
            self._logout()
        return self._play_moves(game_id, moves)

    def _play_moves(self, game_id: str, moves: list):
        """
        For a given game id play some moves.

        :param game_id: The ID of the game.
        :type game_id: str.
        :param moves: All the moves to be played.
        :type moves: list.
        :return: State of the last move.
        """
        move = None
        for m in moves:
            login = self._login(m.get("player"))
            if login.status_code != 202:
                raise SystemError("Login failed during play moves!")
            move = self._client(
                "post",
                f"/v1/games/{game_id}/moves",
                data={
                    "x": m.get("x"),
                    "y": m.get("y"),
                },
            )
            self._logout()
        return move

    def _register(self, player: str):
        """
        Sign up a given player based on symbol.

        :param player: The symbol of the player to register.
        :type player: str.
        :return: Api response of registering the player.
        """
        return self._client("post", "/v1/register", data=self.users[player])

    def _setup_players(self):
        """
        Register all the players in a single loop
        """
        self._register("x")
        self._register("o")
        self._register("z")

    def _setup_game(self) -> str:
        """
        Create a game and set up the players to play the game.

        :return: Game ID.
        :rtype: str.
        """

        game_id = None
        for player in ["x", "o"]:
            self._register(player)
            self._login(player)
            if player == "x":
                game_id = self._games_post()
            self._game_put(game_id, player)
            self._logout()
        return game_id

    def test_game_get(self):
        """
        Create a game and confirm it was created.
        """

        self._setup_players()
        self._login("x")
        game_id = self._games_post()
        game = self._game_get(game_id)
        self._logout()
        self.assertEqual(game.status_code, 200)

    def test_invalid_game_get(self):
        """
        Try getting a game that does not exist.
        """

        self._register("x")
        self._login("x")
        game = self._game_get(str(uuid4()))
        self._logout()
        self.assertEqual(game.status_code, 404)

    def test_games_get(self):
        """
        Try getting a list of games that was created.
        """

        self._register("x")
        self._login("x")
        games = self._client("get", "/v1/games")
        self.assertEqual(games.status_code, 200)

    def test_games_post_good(self):
        """
        Create a game and make sure it was created with a uuid.
        """

        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._logout()
        self.assertEqual(str(UUID(game_id, version=4)) == game_id, True)

    def test_games_post_bad(self):
        """
        Create a game with bad data.
        """

        self._register("x")
        self._login("x")
        game = self._client("post", "/v1/games", data={})
        self.assertEqual(game.status_code, 400)

    def tests_game_move_post(self):
        """
        Make sure we can make a move in the game.
        """

        game_id = self._setup_game()
        self._login("x")
        move = self._client(
            "post",
            f"/v1/games/{game_id}/moves",
            data={
                "x": 0,
                "y": 0,
            },
        )
        self._logout()
        self.assertEqual(move.status_code, 201)

    def test_game_horizontal_win(self):
        """
        Make sure by making moves that we can win horizontally.
        """

        moves = [
            {
                "player": "x",
                "x": 0,
                "y": 0,
            },
            {
                "player": "o",
                "x": 0,
                "y": 2,
            },
            {
                "player": "x",
                "x": 1,
                "y": 0,
            },
            {
                "player": "o",
                "x": 1,
                "y": 2,
            },
            {
                "player": "x",
                "x": 2,
                "y": 0,
            },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEqual(message, "Congratulations x you are the winner!")

    def test_game_vertical_win(self):
        """
        Make sure by making moves that we can win vertically.
        """

        moves = [
            {
                "player": "x",
                "x": 0,
                "y": 0,
            },
            {
                "player": "o",
                "x": 1,
                "y": 1,
            },
            {
                "player": "x",
                "x": 0,
                "y": 1,
            },
            {
                "player": "o",
                "x": 1,
                "y": 2,
            },
            {
                "player": "x",
                "x": 0,
                "y": 2,
            },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEqual(message, "Congratulations x you are the winner!")

    def test_game_back_slash_win(self):
        """
        Make sure by making moves that we can win diagonally from left to right.
        """

        moves = [
            {
                "player": "x",
                "x": 0,
                "y": 0,
            },
            {
                "player": "o",
                "x": 1,
                "y": 0,
            },
            {
                "player": "x",
                "x": 1,
                "y": 1,
            },
            {
                "player": "o",
                "x": 1,
                "y": 2,
            },
            {
                "player": "x",
                "x": 2,
                "y": 2,
            },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEqual(message, "Congratulations x you are the winner!")

    def test_game_forward_slash_win(self):
        """
        Make sure by making moves that we can win diagonally from right to left.
        """

        moves = [
            {
                "player": "x",
                "x": 2,
                "y": 0,
            },
            {
                "player": "o",
                "x": 1,
                "y": 0,
            },
            {
                "player": "x",
                "x": 1,
                "y": 1,
            },
            {
                "player": "o",
                "x": 1,
                "y": 2,
            },
            {
                "player": "x",
                "x": 0,
                "y": 2,
            },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEqual(message, "Congratulations x you are the winner!")

    def test_game_over_x_winner(self):
        """
        See if symbol X is the winner of the game.
        """

        message = self._play_game(
            [
                {
                    "player": "x",
                    "x": 2,
                    "y": 0,
                },
                {
                    "player": "o",
                    "x": 1,
                    "y": 0,
                },
                {
                    "player": "x",
                    "x": 1,
                    "y": 1,
                },
                {
                    "player": "o",
                    "x": 1,
                    "y": 2,
                },
                {
                    "player": "x",
                    "x": 0,
                    "y": 2,
                },
                {
                    "player": "o",
                    "x": 2,
                    "y": 2,
                },
            ]
        ).json()["message"]
        self.assertEqual(message, "Game is over! Player X is the winner!")

    def test_game_over_o_winner(self):
        """
        See if symbol O is the winner of the game.
        """

        message = self._play_game(
            [
                {
                    "player": "x",
                    "x": 2,
                    "y": 2,
                },
                {
                    "player": "o",
                    "x": 2,
                    "y": 0,
                },
                {
                    "player": "x",
                    "x": 1,
                    "y": 0,
                },
                {
                    "player": "o",
                    "x": 1,
                    "y": 1,
                },
                {
                    "player": "x",
                    "x": 1,
                    "y": 2,
                },
                {
                    "player": "o",
                    "x": 0,
                    "y": 2,
                },
                {
                    "player": "x",
                    "x": 0,
                    "y": 0,
                },
            ]
        ).json()["message"]
        self.assertEqual(message, "Game is over! Player O is the winner!")

    def test_game_over_tie(self):
        """
        Fill up the board and make sure it is a tie game.
        """

        move = self._play_game(
            [
                {
                    "player": "x",
                    "x": 0,
                    "y": 0,
                },
                {
                    "player": "o",
                    "x": 2,
                    "y": 0,
                },
                {
                    "player": "x",
                    "x": 1,
                    "y": 0,
                },
                {
                    "player": "o",
                    "x": 0,
                    "y": 1,
                },
                {
                    "player": "x",
                    "x": 0,
                    "y": 2,
                },
                {
                    "player": "o",
                    "x": 2,
                    "y": 2,
                },
                {
                    "player": "x",
                    "x": 1,
                    "y": 1,
                },
                {
                    "player": "o",
                    "x": 1,
                    "y": 2,
                },
                {
                    "player": "x",
                    "x": 2,
                    "y": 1,
                },
                {
                    "player": "o",
                    "x": 0,
                    "y": 0,
                },
            ]
        )
        message = move.json()["message"]
        self.assertEqual(message, "Game is over! Ended in Tie!")

    def test_move_outside_x_axis(self):
        """
        Make sure it is a bad move if we try to move outside the board.
        """

        move = self._play_game(
            [
                {
                    "player": "x",
                    "x": 3,
                    "y": 0,
                }
            ]
        )
        self.assertEqual(move.status_code, 400)

    def test_move_outside_y_axis(self):
        """
        Make sure it is a bad move if we try to move outside the board.
        """

        move = self._play_game(
            [
                {
                    "player": "x",
                    "x": 0,
                    "y": 3,
                }
            ]
        )
        self.assertEqual(move.status_code, 400)

    def test_game_wrong_player_move(self):
        """
        Make sure that player cannot move when it is not their turn.
        """

        move = self._play_game(
            [
                {
                    "player": "x",
                    "x": 0,
                    "y": 0,
                },
                {
                    "player": "x",
                    "x": 0,
                    "y": 1,
                },
            ]
        )
        self.assertEqual(move.status_code, 400)

    def test_game_move_overlap(self):
        """
        Make sure a player cannot move where another player already moved.
        """

        move = self._play_game(
            [
                {
                    "player": "x",
                    "x": 0,
                    "y": 0,
                },
                {
                    "player": "o",
                    "x": 0,
                    "y": 0,
                },
            ]
        )
        self.assertEqual(move.status_code, 400)

    def test_game_invalid_player(self):
        """
        Make sure we cannot take over a spot of another player.
        """

        # todo: clean this up a bit!
        self._setup_players()
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        self._logout()
        self._login("o")
        self._game_put(game_id, "o")
        self._logout()
        self._login("z")
        assign = self._game_put(game_id, "x")
        self.assertEqual(assign.status_code, 400)

    def test_game_invalid_player_move(self):
        """
        Make sure someone cannot play as another player.
        """

        self._setup_players()
        game_id = None
        for player in ["x", "o"]:
            self._login(player)
            if player == "x":
                game_id = self._games_post()
            self._game_put(game_id, player)
            self._logout()
        move = self._play_moves(
            game_id,
            [
                {
                    "player": "z",
                    "x": 0,
                    "y": 0,
                },
            ],
        )
        self.assertEqual(move.status_code, 400)

    def test_register_user_good(self):
        """
        Make sure we can register
        """

        register = self._register("x")
        self.assertEqual(register.status_code, 201)

    def test_register_user_bad(self):
        """
        Register with bad data should fail.
        """

        self.users["x"]["password2"] = self._password_generator(64)
        register = self._register("x")
        self.assertEqual(register.status_code, 400)

    def test_login_good(self):
        """
        Should be able to login here.
        """

        register = self._register("x")
        if register.status_code != 201:
            raise ValueError("We did not register correctly.")
        login = self._login("x")
        self.assertEqual(login.status_code, 202)

    def test_login_bad(self):
        """
        Wrong password should fail.
        """

        self._register("x")
        self.users["x"]["password"] = self._password_generator(64)
        login = self._login("x")
        self.assertEqual(login.status_code, 400)

    def test_logout(self):
        """
        Should be abe to logout.
        """

        register = self._register("x")
        if register.status_code != 201:
            raise ValueError("We did not register correctly.")
        login = self._login("x")
        if login.status_code != 202:
            raise ValueError("We did not login correctly.")
        logout = self._logout()
        self.assertEqual(logout.status_code, 202)

    def test_game_assign_symbol(self):
        """
        Make sure that we can assign a symbol to a player.
        """

        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        data = self._client("get", f"/v1/games/{game_id}").json().get("data")
        player_x = data.get("player_x")
        self.assertEqual(player_x.get("id"), 1)

    def test_game_single_player(self):
        """
        Two payer a needed to play a game not just one.
        """

        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        move = self._client(
            "post",
            f"/v1/games/{game_id}/moves",
            data={
                "x": 0,
                "y": 0,
            },
        )
        self.assertEqual(move.status_code, 400)

    def test_game_same_player(self):
        """
        Player cannot be both X and O.
        """

        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        invalid = self._game_put(game_id, "o")
        self.assertEqual(invalid.status_code, 400)

    def test_moves_get(self):
        """
        See if we can get all the moves for a given game.
        """

        game_id = self._setup_game()
        self._play_moves(
            game_id,
            [
                {
                    "player": "x",
                    "x": 0,
                    "y": 0,
                },
            ],
        )
        self._login("x")
        moves = self._client("get", f"/v1/games/{game_id}/moves")
        self.assertEqual(moves.status_code, 200)

    def test_move_bad(self):
        """
        Try to make am ove with bad data.
        """

        game_id = self._setup_game()
        self._login("x")
        move = self._client("post", f"/v1/games/{game_id}/moves", data={})
        self.assertEqual(move.status_code, 400)

    def test_who(self):
        """
        Can we get who we are?
        """

        self._register("x")
        self._login("x")
        who = self._client("get", "/v1/who").json()
        self.assertEqual(who.get("data")["username"], self.users.get("x")["username"])
