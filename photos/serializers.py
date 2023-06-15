from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Photo
from users.serializers import UserProfileSerializer
from tags.serializers import TinyTagSerializer
from comments.serializers import TinyCommentSerializer


class PhotoListSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = (
            "pk",
            "photo",
            "title",
            "user",
            "tags",
        )


class PhotoDetailSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)
    comments = TinyCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = "__all__"
