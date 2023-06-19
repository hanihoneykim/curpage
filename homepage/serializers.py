from rest_framework import serializers
from photos.serializers import TinyPhotoSerializer
from texts.serializers import TinyTextSerializer
from videos.serializers import TinyVideoSerializer


class HomeSerializer(serializers.Serializer):
    photos = TinyPhotoSerializer(read_only=True, many=True)
    texts = TinyTextSerializer(read_only=True, many=True)
    videos = TinyVideoSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            "photos",
            "texts",
            "videos",
        )
