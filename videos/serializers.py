from rest_framework.serializers import ModelSerializer
from .models import Video
from users.serializers import TinyUserSerializer
from tags.serializers import TinyTagSerializer


class VideoListSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = (
            "pk",
            "video",
            "title",
            "user",
            "tags",
        )


class VideoDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    tags = TinyTagSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = "__all__"
