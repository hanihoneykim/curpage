from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Comment
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
