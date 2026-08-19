from django.urls import path, include

from .views import (
    RegisterView,
    MeView,
    KarraView,
)

urlpatterns = [
    path(
        "api/<str:language>/register/",
        RegisterView.as_view()
    ),

    path(
        "api/<str:language>/me/",
        MeView.as_view()
    ),

    path(
        "api/<str:language>/karra/<int:number>/",
        KarraView.as_view()
    ),
]