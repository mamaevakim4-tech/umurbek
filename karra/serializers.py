from django.contrib.auth.models import User
from rest_framework import serializers

from .models import GameResult, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username", "").strip()

        if not username:
            raise serializers.ValidationError({
                "username": "Username kiriting"
            })

        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({
                "username": "Bu username allaqachon mavjud"
            })

        attrs["username"] = username

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(
            user=user
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )


class UserSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "language",
        ]

    def get_language(self, obj):
        profile, _ = UserProfile.objects.get_or_create(
            user=obj
        )

        return profile.language


class LanguageSerializer(serializers.Serializer):
    language = serializers.ChoiceField(
        choices=["uz", "ru", "en"]
    )


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = [
            "id",
            "level",
            "score",
            "best_streak",
            "created_at",
        ]
