from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Photo
from users.serializers import TinyUserSerializer
from tags.serializers import TinyTagSerializer


class PhotoListSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = (
            "pk",
            "photo",
            "title",
            "description",
            "user",
            "tags",
        )


class PhotoDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = "__all__"
