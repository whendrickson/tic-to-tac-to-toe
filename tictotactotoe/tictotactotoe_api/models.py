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

from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Games(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, default="")
    state = models.CharField(max_length=16, blank=False, default="turn_x")
    player_o = models.ForeignKey(User, to_field="id", related_name="player_o", on_delete=models.DO_NOTHING, null=True)
    player_x = models.ForeignKey(User, to_field="id", related_name="player_x", on_delete=models.DO_NOTHING, null=True)


class Moves(BaseModel):
    PLAYER_CHOICES = (
        ("x", "x"),
        ("o", "o"),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    game = models.ForeignKey(Games, on_delete=models.DO_NOTHING, blank=False)
    player = models.CharField(max_length=1, blank=False, null=False, choices=PLAYER_CHOICES)
    x = models.IntegerField(blank=False)
    y = models.IntegerField(blank=False)
