from rest_framework import serializers
from .models import Text
from tags.serializers import TagListSerializer
from users.serializers import TinyUserSerializer


class TextListSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    tags = TagListSerializer(many=True)
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Text
        fields = (
            "pk",
            "title",
            "user",
            "tags",
            "total_likes",
        )

    def get_total_likes(self, text):
        return text.total_likes()


class TextDetailSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    tags = TagListSerializer(many=True, read_only=True)
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Text
        fields = "__all__"

    def get_total_likes(self, text):
        return text.total_likes()
