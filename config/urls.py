from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from karra.views import (
    RegisterView,
    MeView,
    KarraView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += i18n_patterns(
    path("api/register/", RegisterView.as_view()),
    path("api/me/", MeView.as_view()),
    path("api/karra/<int:number>/", KarraView.as_view()),
)