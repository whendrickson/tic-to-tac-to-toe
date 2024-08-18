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
