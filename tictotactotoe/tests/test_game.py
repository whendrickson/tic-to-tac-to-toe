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
from .test_base import TicToTacToToeApiTestCase


class TicToTacToToeGameTestCases(TicToTacToToeApiTestCase):
    """
    Let's make sure some of the tictactoe game play works.
    """

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
        Two players are needed to play a game not just one.
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
