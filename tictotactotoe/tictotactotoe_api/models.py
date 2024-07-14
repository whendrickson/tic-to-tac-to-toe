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

from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Based model to be used when building models.
    """

    objects = models.Manager()

    class Meta:
        """
        This is a base class so do not build this as a table.
        """

        abstract = True


class Games(BaseModel):
    """
    Tic-Tac-Toe games.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        blank=False,
    )
    state = models.CharField(
        max_length=16,
        blank=False,
        default="turn_x",
    )
    player_o = models.ForeignKey(
        User,
        to_field="id",
        related_name="player_o",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    player_x = models.ForeignKey(
        User,
        to_field="id",
        related_name="player_x",
        on_delete=models.DO_NOTHING,
        null=True,
    )


class Moves(BaseModel):
    """
    Moves that happened in a Tic-Tac-Toe game.
    """

    PLAYER_CHOICES = (
        ("x", "x"),
        ("o", "o"),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    game = models.ForeignKey(
        Games,
        on_delete=models.DO_NOTHING,
        blank=False,
    )
    player = models.CharField(
        max_length=1,
        blank=False,
        null=False,
        choices=PLAYER_CHOICES,
    )
    x = models.IntegerField(
        blank=False,
    )
    y = models.IntegerField(
        blank=False,
    )
