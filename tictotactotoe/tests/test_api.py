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

from django.test import TestCase
from uuid import UUID, uuid4
import json


class TicToTacToToeApiTestCase(TestCase):

    def setUp(self):
        self.users = {
            "x": {
                "username": "test001",
                "password": "password123!",
                "password2": "password123!",
                "email": "email001@email.com",
                "first_name": "first001",
                "last_name": "last001",
            },
            "o": {
                "username": "test002",
                "password": "password123!",
                "password2": "password123!",
                "email": "email002@email.com",
                "first_name": "first002",
                "last_name": "last002",
            },
            "z": {
                "username": "test003",
                "password": "password123!",
                "password2": "password123!",
                "email": "email003@email.com",
                "first_name": "first003",
                "last_name": "last003",
            },
        }

    def tearDown(self):
        pass

    def test_true(self):
        self.assertTrue(True)

    def _client(self, method, uri, **kwargs):
        if not uri.startswith("/api"):
            uri = f"/api{uri}"
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
        return getattr(self.client, method)(uri, content_type="application/json", **kwargs)

    def _game_get(self, game_id):
        return self._client("get", f"/v1/games/{game_id}")

    def _game_put(self, game_id, player):
        return self._client("put", f"/v1/games/{game_id}", data={
            "player": player,
        })

    def _games_post(self):
        # typically we just want the game id so send it back
        game = self._client("post", "/v1/games", data={
            "name": "test001",
        })
        return game.json()["data"]["id"]

    def _login(self, player):
        data = {
            "username": self.users[player].get("username"),
            "password": self.users[player].get("password"),
        }
        return self._client("post", "/v1/login", data=data)

    def _logout(self):
        return self._client("post", "/v1/logout", data={})

    def _play_game(self, moves):
        self._setup_players()
        self._login("x")
        game_id = self._games_post()
        self._logout()
        for player in ["x", "o"]:
            self._login(player)
            self._game_put(game_id, player)
            self._logout()
        move = self._play_moves(game_id, moves)
        return move

    def _play_moves(self, game_id, moves):
        move = None
        for m in moves:
            login = self._login(m.get("player"))
            if login.status_code != 202:
                raise Exception("Login failed during play moves!")
            move = self._client("post", f"/v1/games/{game_id}/moves", data={
                "x": m.get("x"),
                "y": m.get("y"),
            })
            self._logout()
        return move

    def _register(self, player):
        return self._client("post", "/v1/register", data=self.users[player])

    def _setup_players(self):
        self._register("x")
        self._register("o")
        self._register("z")

    def _setup_game(self):
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
        self._setup_players()
        self._login("x")
        game_id = self._games_post()
        game = self._game_get(game_id)
        self._logout()
        self.assertEquals(game.status_code, 200)

    def test_invalid_game_get(self):
        self._register("x")
        self._login("x")
        game = self._game_get(uuid4())
        self._logout()
        self.assertEquals(game.status_code, 404)

    def test_games_get(self):
        self._register("x")
        self._login("x")
        games = self._client("get", "/v1/games")
        self.assertEquals(games.status_code, 200)

    def test_games_post_good(self):
        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._logout()
        self.assertEquals(str(UUID(game_id, version=4)) == game_id, True)

    def test_games_post_bad(self):
        self._register("x")
        self._login("x")
        game = self._client("post", "/v1/games", data={})
        self.assertEquals(game.status_code, 400)

    def tests_game_move_post(self):
        # can a move be made?
        game_id = self._setup_game()
        self._login("x")
        move = self._client("post", f"/v1/games/{game_id}/moves", data={
            "x": 0,
            "y": 0,
        })
        self._logout()
        self.assertEquals(move.status_code, 201)

    def test_game_horizontal_win(self):
        moves = [
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 0, "y": 2, },
            {"player": "x", "x": 1, "y": 0, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 2, "y": 0, },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEquals(message, "Congratulations x you are the winner!")

    def test_game_vertical_win(self):
        moves = [
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 1, "y": 1, },
            {"player": "x", "x": 0, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 0, "y": 2, },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEquals(message, "Congratulations x you are the winner!")

    def test_game_back_slash_win(self):
        moves = [
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 1, "y": 0, },
            {"player": "x", "x": 1, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 2, "y": 2, },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEquals(message, "Congratulations x you are the winner!")

    def test_game_forward_slash_win(self):
        moves = [
            {"player": "x", "x": 2, "y": 0, },
            {"player": "o", "x": 1, "y": 0, },
            {"player": "x", "x": 1, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 0, "y": 2, },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEquals(message, "Congratulations x you are the winner!")

    def test_game_tie(self):
        moves = [
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 2, "y": 0, },
            {"player": "x", "x": 1, "y": 0, },
            {"player": "o", "x": 0, "y": 1, },
            {"player": "x", "x": 0, "y": 2, },
            {"player": "o", "x": 2, "y": 2, },
            {"player": "x", "x": 1, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 2, "y": 1, },
        ]
        message = self._play_game(moves).json()["message"]
        self.assertEquals(message, "Full board! Game ended in a tie.")

    def test_game_over_x_winner(self):
        message = self._play_game([
            {"player": "x", "x": 2, "y": 0, },
            {"player": "o", "x": 1, "y": 0, },
            {"player": "x", "x": 1, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 0, "y": 2, },
            {"player": "o", "x": 2, "y": 2, },
        ]).json()["message"]
        self.assertEquals(message, "Game is over! Player X is the winner!")

    def test_game_over_o_winner(self):
        message = self._play_game([
            {"player": "x", "x": 2, "y": 2, },
            {"player": "o", "x": 2, "y": 0, },
            {"player": "x", "x": 1, "y": 0, },
            {"player": "o", "x": 1, "y": 1, },
            {"player": "x", "x": 1, "y": 2, },
            {"player": "o", "x": 0, "y": 2, },
            {"player": "x", "x": 0, "y": 0, },
        ]).json()["message"]
        self.assertEquals(message, "Game is over! Player O is the winner!")

    def test_game_over_tie(self):
        move = self._play_game([
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 2, "y": 0, },
            {"player": "x", "x": 1, "y": 0, },
            {"player": "o", "x": 0, "y": 1, },
            {"player": "x", "x": 0, "y": 2, },
            {"player": "o", "x": 2, "y": 2, },
            {"player": "x", "x": 1, "y": 1, },
            {"player": "o", "x": 1, "y": 2, },
            {"player": "x", "x": 2, "y": 1, },
            {"player": "o", "x": 0, "y": 0, },
        ])
        message = move.json()["message"]
        self.assertEquals(message, "Game is over! Ended in Tie!")

    def test_move_outside_x_axis(self):
        move = self._play_game([{"player": "x", "x": 3, "y": 0, }])
        self.assertEquals(move.status_code, 400)

    def test_move_outside_y_axis(self):
        move = self._play_game([{"player": "x", "x": 0, "y": 3, }])
        self.assertEquals(move.status_code, 400)

    def test_game_wrong_player_move(self):
        move = self._play_game([
            {"player": "x", "x": 0, "y": 0, },
            {"player": "x", "x": 0, "y": 1, },
        ])
        self.assertEquals(move.status_code, 400)

    def test_game_move_overlap(self):
        move = self._play_game([
            {"player": "x", "x": 0, "y": 0, },
            {"player": "o", "x": 0, "y": 0, },
        ])
        self.assertEquals(move.status_code, 400)

    def test_game_invalid_player(self):
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
        self.assertEquals(assign.status_code, 400)

    def test_game_invalid_player_move(self):
        self._setup_players()
        game_id = None
        for player in ["x", "o"]:
            self._login(player)
            if player == "x":
                game_id = self._games_post()
            self._game_put(game_id, player)
            self._logout()
        move = self._play_moves(game_id, [{"player": "z", "x": 0, "y": 0, }, ])
        self.assertEquals(move.status_code, 400)

    def test_register_user_good(self):
        register = self._register("x")
        self.assertEquals(register.status_code, 201)

    def test_register_user_bad(self):
        self.users["x"]["password2"] = "SuperBadPassword!123"
        register = self._register("x")
        self.assertEquals(register.status_code, 400)

    def test_login_good(self):
        register = self._register("x")
        if register.status_code != 201:
            raise ValueError("We did not register correctly.")
        login = self._login("x")
        self.assertEquals(login.status_code, 202)

    def test_login_bad(self):
        self._register("x")
        self.users["x"]["password"] = "SuperBadPassword!123"
        login = self._login("x")
        self.assertEquals(login.status_code, 400)

    def test_logout(self):
        register = self._register("x")
        if register.status_code != 201:
            raise ValueError("We did not register correctly.")
        login = self._login("x")
        if login.status_code != 202:
            raise ValueError("We did not login correctly.")
        logout = self._logout()
        self.assertEquals(logout.status_code, 202)

    def test_game_assign_symbol(self):
        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        player_x = self._client("get", f"/v1/games/{game_id}").json()["data"]["player_x"]
        self.assertEquals(player_x.get("id"), 1)

    def test_game_single_player(self):
        # before allowing a move make sure both players a set
        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        move = self._client("post", f"/v1/games/{game_id}/moves", data={
            "x": 0,
            "y": 0,
        })
        self.assertEquals(move.status_code, 400)

    def test_game_same_player(self):
        self._register("x")
        self._login("x")
        game_id = self._games_post()
        self._game_put(game_id, "x")
        invalid = self._game_put(game_id, "o")
        self.assertEquals(invalid.status_code, 400)

    def test_moves_get(self):
        game_id = self._setup_game()
        self._play_moves(game_id, [{"player": "x", "x": 0, "y": 0, }, ])
        self._login("x")
        moves = self._client("get", f"/v1/games/{game_id}/moves")
        self.assertEquals(moves.status_code, 200)

    def test_move_bad(self):
        game_id = self._setup_game()
        self._login("x")
        move = self._client("post", f"/v1/games/{game_id}/moves", data={})
        self.assertEquals(move.status_code, 400)

    def test_who(self):
        self._register("x")
        self._login("x")
        who = self._client("get", "/v1/who").json()
        self.assertEquals(who.get("data")["username"], self.users.get("x")["username"])

