from rest_framework import serializers


class MultiplicationSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    question = serializers.CharField()
    answer = serializers.IntegerField()