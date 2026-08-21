from django.contrib import admin

from .models import Game, GameResult, UserProfile

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(GameResult)