from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from karra.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    LanguageAPIView,
    GameStartAPIView,
    GameAnswerAPIView,
    GameResultAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/register/", RegisterAPIView.as_view()),
    path("api/login/", LoginAPIView.as_view()),
    path("api/logout/", LogoutAPIView.as_view()),
    path("api/me/", MeAPIView.as_view()),
    path("api/language/", LanguageAPIView.as_view()),
    path("api/game/start/", GameStartAPIView.as_view()),
    path("api/game/answer/", GameAnswerAPIView.as_view()),
    path("api/game/result/", GameResultAPIView.as_view()),
]