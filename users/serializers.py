from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)


class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "name",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_photo",
        )


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
    count_texts = serializers.SerializerMethodField(read_only=True)
    count_photos = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    count_followers = serializers.SerializerMethodField(read_only=True)
    count_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "profile_photo",
            "name",
            "username",
            "total_texts",
            "total_photos",
            "total_videos",
            "count_texts",
            "count_photos",
            "following",
            "followers",
            "is_following",
            "count_followers",
            "count_following",
        )

    def get_total_texts(self, user):
        users_texts = user.texts.all()
        return [
            {
                "title": text.title,
                "pk": text.pk,
                # 다른 원하는 속성들도 추가할 수 있음
            }
            for text in users_texts
        ]

    def get_total_photos(self, user):
        users_photos = user.photos.all()
        return [
            {
                "image_url": photo.photo,  # 예시로 image_url을 가져오는 방법
                "pk": photo.pk,
                # 다른 원하는 속성들도 추가할 수 있음
            }
            for photo in users_photos
        ]

    def get_total_videos(self, user):
        return user.videos.count()

    def get_count_texts(self, user):
        return user.texts.count()

    def get_count_photos(self, user):
        return user.photos.count()

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

    def get_count_following(self, user):
        return user.following.count()

    def get_count_followers(self, user):
        return user.following.count()


class signUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
        )


class MyLikesSerializer(serializers.ModelSerializer):
    likes_photos = serializers.SerializerMethodField(read_only=True)
    likes_texts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("likes_photos", "likes_texts")

    def get_likes_photos(self, user):
        likes = user.likes.filter(photo__isnull=False)
        serialized_likes = []

        for like in likes:
            serialized_like = {
                "photo_pk": like.photo.id if like.photo else None,
                "photo_url": like.photo.photo if like.photo else None,
            }
            serialized_likes.append(serialized_like)

        return serialized_likes

    def get_likes_texts(self, user):
        likes = user.likes.filter(text__isnull=False)
        serialized_likes = []

        for like in likes:
            serialized_like = {
                "text_pk": like.text.id if like.text else None,
                "text_title": like.text.title if like.text else None,
            }
            serialized_likes.append(serialized_like)

        return serialized_likes


class MyBookmarksSerializer(serializers.ModelSerializer):
    bookmarks_photos = serializers.SerializerMethodField(read_only=True)
    bookmarks_texts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("bookmarks_photos", "bookmarks_texts")

    def get_bookmarks_photos(self, user):
        bookmarks = user.bookmarks.filter(photo__isnull=False)
        serialized_bookmarks = []

        for bookmark in bookmarks:
            serialized_bookmark = {
                "photo_pk": bookmark.photo.id if bookmark.photo else None,
                "photo_url": bookmark.photo.photo if bookmark.photo else None,
            }
            serialized_bookmarks.append(serialized_bookmark)

        return serialized_bookmarks

    def get_bookmarks_texts(self, user):
        bookmarks = user.bookmarks.filter(text__isnull=False)
        serialized_bookmarks = []

        for bookmark in bookmarks:
            serialized_bookmark = {
                "text_pk": bookmark.text.id if bookmark.text else None,
                "text_title": bookmark.text.title if bookmark.text else None,
            }
            serialized_bookmarks.append(serialized_bookmark)

        return serialized_bookmarks
