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


class TicToTacToToeAuthTestCases(TicToTacToToeApiTestCase):
    """
    Let's see if registration works and sign-in and sign-out.
    """

    def test_login_good(self):
        """
        Should be able to log in here.
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

    def test_register_email_case_overlap(self):
        """
        Email address should not be case-sensitive.
        """

        self._register("x")
        self.users["o"]["email"] = self.users["x"]["email"].title()
        register = self._register("o")
        self.assertEqual(register.status_code, 400)

    def test_register_user_bad(self):
        """
        Register with bad data should fail.
        """

        self.users["x"]["password2"] = self._password_generator(64)
        register = self._register("x")
        self.assertEqual(register.status_code, 400)

    def test_register_user_case_overlap(self):
        """
        Username should not be case-sensitive.
        """

        self._register("x")
        self.users["x"]["username"] = self.users["x"]["username"].title()
        # need a different email as emails cannot overlap
        self.users["x"]["email"] = "different_username@testcase.com"
        register = self._register("x")
        self.assertEqual(register.status_code, 400)

    def test_register_user_good(self):
        """
        Make sure we can register.
        """

        register = self._register("x")
        self.assertEqual(register.status_code, 201)

    def test_register_user_too_long(self):
        """
        Username should be max 30 characters long.
        """

        self.users["x"]["username"] = "abcdefghijklmnopqrstuvwxyzabcde"
        register = self._register("x")
        self.assertEqual(register.status_code, 400)

    def test_register_user_too_short(self):
        """
        Username should be at least 6 characters long.
        """

        self.users["x"]["username"] = "a"
        register = self._register("x")
        self.assertEqual(register.status_code, 400)

    def test_who(self):
        """
        Can we get who we are?
        """

        self._register("x")
        self._login("x")
        who = self._client("get", "/v1/who").json()
        self.assertEqual(who.get("data")["username"], self.users.get("x")["username"])
