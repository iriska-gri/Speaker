from rest_framework import serializers


class DepDirsUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class CallTypeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()