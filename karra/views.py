from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )

        return user


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "success": True,
                "message": _(
                    "Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi."
                )
            })

        return Response(
            serializer.errors,
            status=400
        )


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        })


class KarraView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, number):

        if number < 1 or number > 10:

            return Response({
                "success": False,
                "message": _(
                    "Karra 1 dan 10 gacha bo'lishi kerak."
                )
            }, status=400)

        data = []

        for i in range(1, 11):

            data.append({
                "number": i,
                "question": f"{number} x {i}",
                "answer": number * i
            })

        return Response({
            "success": True,
            "table": number,
            "language": request.LANGUAGE_CODE,
            "data": data
        })