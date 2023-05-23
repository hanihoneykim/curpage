from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)


class PrivateUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)

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

    def get_following(self, user):
        following_users = user.following.all()
        return [following.username for following in following_users]

    def get_followers(self, user):
        followers_users = user.followers.all()
        return [follower.username for follower in followers_users]


class PublicUserSerializer(serializers.ModelSerializer):
    total_texts = serializers.SerializerMethodField(read_only=True)
    total_photos = serializers.SerializerMethodField(read_only=True)
    total_videos = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "profile_photo",
            "name",
            "username",
            "total_texts",
            "total_photos",
            "total_videos",
            "following",
            "followers",
            "is_following",
        )

    def get_total_texts(self, user):
        return user.texts.count()

    def get_total_photos(self, user):
        return user.photos.count()

    def get_total_videos(self, user):
        return user.videos.count()

    def get_following(self, user):
        following_users = user.following.all()
        return [following.username for following in following_users]

    def get_followers(self, user):
        followers_users = user.followers.all()
        return [follower.username for follower in followers_users]

    def get_is_following(self, user):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return user.followers.filter(id=request.user.id).exists()
        return False
