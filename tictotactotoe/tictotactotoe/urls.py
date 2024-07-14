"""
URL configuration for tictotactotoe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def custom400(request, exception=None):
    """
    Json Response HTTP 400
    """

    return JsonResponse(
        data={
            "error": "Bad Request",
        },
        status=400,
    )


def custom403(request, exception=None):
    """
    Json Response HTTP 403
    """

    return JsonResponse(
        data={
            "data": {},
            "status": "error",
            "message": "Permission Denied",
        },
        status=403,
    )


def custom404(request, exception=None):
    """
    Json Response HTTP 404
    """

    return JsonResponse(
        data={
            "error": f"The resource at {request.path} with method {request.method} was not found.",
        },
        status=404,
    )


def custom500(request, exception=None):
    """
    Json Response HTTP 500
    """

    return JsonResponse(
        data={
            "data": {},
            "status": "error",
            "message": "Internal Server Error",
        },
        status=500,
    )


handler400 = custom400
handler403 = custom403
handler404 = custom404
handler500 = custom500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tictotactotoe_api.urls")),
]
