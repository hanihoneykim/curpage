from rest_framework import serializers
from .models import Text
from tags.serializers import TinyTagSerializer
from users.serializers import TinyUserSerializer, UserProfileSerializer
from comments.serializers import CommentSerializer


class TextListSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Text
        fields = (
            "pk",
            "title",
            "body",
            "user",
            "tags",
            "total_likes",
            "comments_count",
        )

    def get_total_likes(self, text):
        return text.total_likes()

    def comments_count(self, text):
        return text.comments_count()


class TextDetailSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Text
        fields = "__all__"

    def get_total_likes(self, text):
        return text.total_likes()

    def comments_count(self, text):
        return text.comments_count()


class TinyTextSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Text
        fields = (
            "pk",
            "title",
            "user",
        )
