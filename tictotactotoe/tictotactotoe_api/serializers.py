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

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Games, Moves


class MoveSerializer(serializers.ModelSerializer):
    """
    Moves that happened in a Tic-Tac-Toe game.
    """

    class Meta:
        """
        Move meta data.
        """

        model = Moves
        fields = [
            "player",
            "x",
            "y",
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Using built-in Django users for game users.
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        """
        User meta data.
        """

        model = User
        fields = (
            "id",
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",  # probably want to look at owasp
                }
            )
        return attrs

    @staticmethod
    def validate_email(value):
        """
        Validate the incoming email address for a user

        :param value: email address
        :return: lowered email address
        """

        email = value.lower()
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass  # awesome the email isn't currently in the db
        else:
            raise serializers.ValidationError(
                {
                    "email": "email is not valid",  # probably want to look at owasp
                }
            )
        return email

    @staticmethod
    def validate_username(value):
        """
        Validate the incoming username for a user

        :param value: username
        :return: lowered username
        """

        username = value.lower()

        if 5 < len(username) < 31:
            pass  # Username is 6–30 characters long
        else:
            raise serializers.ValidationError(
                {
                    "username": "username is not valid",  # probably want to look at owasp
                }
            )

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass  # awesome the username isn't currently in the db
        else:
            raise serializers.ValidationError(
                {
                    "username": "username is not valid",  # probably want to look at owasp
                }
            )
        return username

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class GameSerializer(serializers.ModelSerializer):
    """
    Tic-Tac-Toe games.
    """

    player_o = UserSerializer(read_only=True)
    player_x = UserSerializer(read_only=True)

    class Meta:
        """
        Game meta data.
        """

        model = Games
        fields = (
            "id",
            "name",
            "state",
            "player_o",
            "player_x",
        )


class LoginSerializer(serializers.Serializer):
    # pylint: disable=W0223
    """
    User logging into the application.
    """

    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    # pylint: disable=W0223
    """
    User logging out of the application.
    """
