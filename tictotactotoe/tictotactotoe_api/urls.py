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

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.urlpatterns import format_suffix_patterns
from .views import viewtictactoe
from .views import viewauth

urlpatterns = [
    path(
        "v1/games",
        viewtictactoe.GamesView.as_view(),
    ),
    path(
        "v1/games/<str:game_id>",
        viewtictactoe.GameView.as_view(),
    ),
    path(
        "v1/games/<str:game_id>/moves",
        viewtictactoe.MovesView.as_view(),
    ),
    path(
        "v1/login",
        viewauth.LoginApiView.as_view(),
    ),
    path(
        "v1/logout",
        viewauth.LogoutApiView.as_view(),
    ),
    path(
        "v1/register",
        viewauth.RegisterView.as_view(),
    ),
    path(
        "v1/who",
        viewauth.WhoView.as_view(),
    ),
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
