import random

from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Game, GameResult, UserProfile
from .serializers import (
    GameResultSerializer,
    LanguageSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


def create_question(game):
    if game.level == "easy":
        first = random.randint(1, 5)
        second = random.randint(1, 10)
    elif game.level == "medium":
        first = random.randint(2, 10)
        second = random.randint(2, 10)
    else:
        first = random.randint(6, 20)
        second = random.randint(6, 20)

    game.first_number = first
    game.second_number = second
    game.answer = first * second
    game.save()

    return {
        "question": f"{first} x {second} = ?",
        "question_number": game.question_number,
        "streak": game.streak,
        "score": game.score,
    }


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": _("Registration successful"),
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {
                    "error": _("Invalid username or password")
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": _("Login successful"),
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        logout(request)

        return Response(
            {
                "message": _("Logout successful")
            }
        )


class MeAPIView(APIView):
    def get(self, request):
        return Response(
            UserSerializer(request.user).data
        )


class LanguageAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        return Response(
            {
                "languages": [
                    {
                        "code": "uz",
                        "name": "O'zbek",
                    },
                    {
                        "code": "ru",
                        "name": "Русский",
                    },
                    {
                        "code": "en",
                        "name": "English",
                    },
                ]
            }
        )

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user
        )

        serializer = LanguageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.language = serializer.validated_data["language"]
        profile.save()

        return Response(
            {
                "message": _("Language changed"),
                "language": profile.language,
            }
        )


class GameStartAPIView(APIView):
    def get(self, request):
        return Response(
            {
                "message": _("Choose game level"),
                "levels": [
                    "easy",
                    "medium",
                    "hard",
                ],
            }
        )

    def post(self, request):
        level = request.data.get("level")

        if level not in ["easy", "medium", "hard"]:
            return Response(
                {
                    "error": _(
                        "Level must be easy, medium or hard"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        Game.objects.filter(
            user=request.user,
            finished=False,
        ).update(finished=True)

        game = Game.objects.create(
            user=request.user,
            level=level,
        )

        return Response(
            {
                "message": _("Game started"),
                "game_id": game.id,
                "level": game.level,
                **create_question(game),
            },
            status=status.HTTP_201_CREATED,
        )


class GameAnswerAPIView(APIView):
    def get(self, request):
        game = Game.objects.filter(
            user=request.user,
            finished=False,
        ).order_by("-id").first()

        if not game:
            return Response(
                {
                    "message": _("No active game")
                }
            )

        return Response(
            {
                "game_id": game.id,
                "level": game.level,
                "question": f"{game.first_number} x {game.second_number} = ?",
                "question_number": game.question_number,
                "streak": game.streak,
                "score": game.score,
            }
        )

    def post(self, request):
        game_id = request.data.get("game_id")
        answer = request.data.get("answer")

        if game_id is None or answer is None:
            return Response(
                {
                    "error": _(
                        "game_id and answer are required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            game = Game.objects.get(
                id=game_id,
                user=request.user,
            )
        except Game.DoesNotExist:
            return Response(
                {
                    "error": _("Game not found")
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if game.finished:
            return Response(
                {
                    "error": _("Game is finished")
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            answer = int(answer)
        except (ValueError, TypeError):
            return Response(
                {
                    "error": _("Answer must be a number")
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        correct = answer == game.answer

        if correct:
            game.score += 1
            game.streak += 1

            if game.streak > game.best_streak:
                game.best_streak = game.streak
        else:
            game.streak = 0

        if game.question_number >= 10:
            game.finished = True
            game.save()

            GameResult.objects.create(
                user=request.user,
                level=game.level,
                score=game.score,
                best_streak=game.best_streak,
            )

            if game.score >= 8:
                message = _("Ofarin! Juda yaxshi natija!")
            elif game.score >= 5:
                message = _("Yaxshi! Yana biroz mashq qiling.")
            else:
                message = _("Ko'p xato qildingiz. Yana mashq qiling.")

            return Response(
                {
                    "correct": correct,
                    "correct_answer": game.answer,
                    "score": game.score,
                    "best_streak": game.best_streak,
                    "total_questions": 10,
                    "finished": True,
                    "message": message,
                }
            )

        game.question_number += 1
        game.save()

        return Response(
            {
                "correct": correct,
                "correct_answer": game.answer,
                "message": (
                    _("To'g'ri!")
                    if correct
                    else _("Noto'g'ri!")
                ),
                "finished": False,
                **create_question(game),
            }
        )


class GameResultAPIView(APIView):
    def get(self, request):
        results = GameResult.objects.filter(
            user=request.user
        ).order_by("-created_at")

        return Response(
            GameResultSerializer(
                results,
                many=True,
            ).data
        )
