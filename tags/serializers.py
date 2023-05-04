from rest_framework import serializers
from .models import Tag


class TagListSerializer(serializers.ModelSerializer):
    texts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
            "texts",
        )


class TinyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
        )
