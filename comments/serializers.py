from rest_framework import serializers
from rest_framework import generics
from users.serializers import TinyUserSerializer
from .models import Comment, Like
from texts.models import Text


class CommentSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    text = serializers.PrimaryKeyRelatedField(queryset=Text.objects.all())

    class Meta:
        model = Comment
        fields = (
            "pk",
            "comment",
            "user",
            "text",
        )


class TinyCommentSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "comment",
            "user",
        )


class LikeSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("user",)
