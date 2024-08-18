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

from .test_base import TicToTacToToeApiTestCase


class TicToTacToToeMoveTestCases(TicToTacToToeApiTestCase):
    """
    Let's make sure some of the tictactoe moves works.
    """

    def tests_game_move_post(self):
        """
        Make sure we can make a move in the game.
        """

        game_id = self._setup_game()
        move = self._play_moves(game_id, [{
            "player": "x",
            "x": 0,
            "y": 0,
        }])
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
