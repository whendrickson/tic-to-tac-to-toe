from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .base import TicToTacToToeAPIView
from ..serializers import UserSerializer, LoginSerializer, LogoutSerializer


class LoginApiView(TicToTacToToeAPIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        user = authenticate(
            request,
            **{
                "username": request.data.get("username"),
                "password": request.data.get("password")
            },
        )
        if user is None:
            return self._response(
                message="Invalid credentials.",
                response_code=status.HTTP_400_BAD_REQUEST,
                status_message="error",
            )
        login(request, user)
        self.log.debug(f"{user} - Valid username/password combination.")
        return self._response(
            message="Success kid is successful!",
            response_code=status.HTTP_202_ACCEPTED,
            status_message="ok",
        )


class LogoutApiView(TicToTacToToeAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LogoutSerializer

    def post(self, request, **kwargs):
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
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer


class WhoView(TicToTacToToeAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        u = User.objects.get(id=request.user.id)
        serializer = UserSerializer(u, many=False)
        return self._response(
            data=serializer.data,
            message="This is who you are!",
            response_code=status.HTTP_200_OK,
            status_message="ok",
        )
