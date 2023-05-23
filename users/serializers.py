from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "dmrooms",
        )


class PublicUserSerializer(serializers.ModelSerializer):
    total_texts = serializers.SerializerMethodField(read_only=True)
    total_photos = serializers.SerializerMethodField(read_only=True)
    total_videos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "profile_photo",
            "name",
            "username",
            "total_texts",
            "total_photos",
            "total_videos",
        )

    def get_total_texts(self, user):
        return user.texts.count()

    def get_total_photos(self, user):
        return user.photos.count()

    def get_total_videos(self, user):
        return user.videos.count()
