from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=2,
        choices=[
            ("uz", "O'zbek"),
            ("ru", "Русский"),
            ("en", "English"),
        ],
        default="uz",
    )

    def __str__(self):
        return self.user.username


class Game(models.Model):
    LEVELS = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LEVELS)
    question_number = models.PositiveIntegerField(default=1)
    first_number = models.PositiveIntegerField(default=1)
    second_number = models.PositiveIntegerField(default=1)
    answer = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.level}"


class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10)
    score = models.PositiveIntegerField()
    best_streak = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"