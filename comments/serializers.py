from rest_framework import serializers
from rest_framework import generics
from users.serializers import TinyUserSerializer, LikeUserSerializer
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
    user = LikeUserSerializer(read_only=True)
    count_likes = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Like
        fields = (
            "user",
            "count_likes",
            "is_like",
        )

    def get_count_likes(self, like):
        # Like 모델에서 photo 필드를 통해 연결된 Photo 모델의 좋아요 수를 반환합니다.
        return like.photo.likes.filter(like=True).count()

    def get_is_like(self, like):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            # Like 모델에서 user 필드를 통해 연결된 User 모델과 request.user를 비교하여 True 또는 False를 반환합니다.
            return like.user == request.user
        return False  # 사용자가 로그인하지 않은 경우 기본값은 False입니다.
