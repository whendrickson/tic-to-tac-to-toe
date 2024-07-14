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

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .base import TicToTacToToeAPIView
from ..serializers import UserSerializer, LoginSerializer, LogoutSerializer


class LoginApiView(TicToTacToToeAPIView):
    """
    View for logging into the application.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        """
        Logging into the application.

        :param request:
        :param kwargs:
        :return:
        """

        user = authenticate(
            request,
            **{
                "username": request.data.get("username"),
                "password": request.data.get("password"),
            },
        )
        if user is None:
            return self._response(
                message="Invalid credentials.",
                response_code=status.HTTP_400_BAD_REQUEST,
                status_message="error",
            )
        login(request, user)
        self.log.debug("%s - Valid username/password combination.", user)
        return self._response(
            message="Success kid is successful!",
            response_code=status.HTTP_202_ACCEPTED,
            status_message="ok",
        )


class LogoutApiView(TicToTacToToeAPIView):
    """
    View for logging out of the application.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, **kwargs):
        """
        Logging out of the application.

        :param request:
        :param kwargs:
        :return:
        """

        user = str(request.user)
        logout(request)
        message = f"User {user} has logged out successfully! bye-bye."
        self.log.debug(message)
        return self._response(
            message=message,
            response_code=status.HTTP_202_ACCEPTED,
            status_message="ok",
        )


class RegisterView(generics.CreateAPIView):
    """
    View for registering a user.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class WhoView(TicToTacToToeAPIView):
    """
    Authenticated user to see who they are.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        """
        Get current user.

        :param request:
        :param kwargs:
        :return:
        """

        u = User.objects.get(id=request.user.id)
        serializer = UserSerializer(u, many=False)
        return self._response(
            data=serializer.data,
            message="This is who you are!",
            response_code=status.HTTP_200_OK,
            status_message="ok",
        )
