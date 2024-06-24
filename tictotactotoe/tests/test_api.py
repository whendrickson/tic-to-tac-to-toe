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
        return self._client("post", "/v1/games", data={
            "name": "test001",
        })

    def _login(self, player):
        data = {
            "username": self.users[player].get("username"),
            "password": self.users[player].get("password"),
        }
        return self._client("post", "/v1/login", data=data)

    def _logout(self):
        return self._client("post", "/v1/logout", data={})

    def _play_game(self, moves):
        self._register("x")
        self._register("o")
        self._login("x")
        game = self._games_post()
        game_id = game.json()["data"]["id"]
        self._game_put(game_id, "x")
        self._logout()
        self._login("o")
        self._game_put(game_id, "o")
        self._logout()
        move = None
        for m in moves:
            self._login(m.get("player"))
            move = self._client("post", f"/v1/games/{game_id}/moves", data={
                "x": m.get("x"),
                "y": m.get("y"),
            })
            self._logout()
        return move

    def _register(self, player):
        return self._client("post", "/v1/register", data=self.users[player])

    def test_games_get(self):
        self._register("x")
        self._login("x")
        r = self._client("get", "/v1/games")
        self._logout()
        self.assertEquals(r.status_code, 200)

    def test_game_get(self):
        self._register("x")
        self._login("x")
        create = self._games_post()
        game_id = create.json()["data"]["id"]
        game = self._game_get(game_id)
        self._logout()
        self.assertEquals(game.status_code, 200)

    def test_games_post(self):
        self._register("x")
        self._login("x")
        r = self._games_post()
        self._logout()
        self.assertEquals(r.status_code, 201)

    def tests_game_move_post(self):
        # can a move be made?
        self._register("x")
        self._register("o")
        self._login("x")
        game = self._games_post()
        game_id = game.json()["data"]["id"]
        self._game_put(game_id, "x")
        self._logout()
        self._login("o")
        self._game_put(game_id, "o")
        self._logout()
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
        self._register("x")
        self._register("o")
        self._register("z")
        self._login("x")
        game = self._games_post()
        game_id = game.json()["data"]["id"]
        self._game_put(game_id, "x")
        self._logout()
        self._login("o")
        self._game_put(game_id, "o")
        self._logout()
        self._login("z")
        assign = self._game_put(game_id, "x")
        self.assertEquals(assign.status_code, 400)

    def test_register_user(self):
        register = self._register("x")
        self.assertEquals(register.status_code, 201)

    def test_login(self):
        register = self._register("x")
        if register.status_code != 201:
            raise ValueError("We did not register correctly.")
        login = self._login("x")
        self.assertEquals(login.status_code, 202)

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
        game = self._games_post()
        game_id = game.json()["data"]["id"]
        self._game_put(game_id, "x")
        player_x = self._client("get", f"/v1/games/{game_id}").json()["data"]["player_x"]
        self.assertEquals(player_x.get("id"), 1)

    def test_game_single_player(self):
        # before allowing a move make sure both players a set
        self._register("x")
        self._login("x")
        game = self._games_post()
        game_id = game.json()["data"]["id"]
        self._game_put(game_id, "x")
        move = self._client("post", f"/v1/games/{game_id}/moves", data={
            "x": 0,
            "y": 0,
        })
        self.assertEquals(move.status_code, 400)

    def test_who(self):
        self._register("x")
        self._login("x")
        who = self._client("get", "/v1/who").json()
        self.assertEquals(who.get("data")["username"], self.users.get("x")["username"])

