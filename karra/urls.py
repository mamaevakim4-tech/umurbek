from django.urls import path

from .views import (
    GameAnswerAPIView,
    GameResultAPIView,
    GameStartAPIView,
    LanguageAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
    ),
    path(
        "login/",
        LoginAPIView.as_view(),
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
    ),
    path(
        "me/",
        MeAPIView.as_view(),
    ),
    path(
        "language/",
        LanguageAPIView.as_view(),
    ),
    path(
        "game/start/",
        GameStartAPIView.as_view(),
    ),
    path(
        "game/answer/",
        GameAnswerAPIView.as_view(),
    ),
    path(
        "game/results/",
        GameResultAPIView.as_view(),
    ),
]