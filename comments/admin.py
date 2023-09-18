from django.contrib import admin
from .models import Comment, Like, Bookmark


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "created_at",
    )

    search_fields = ("=user__username",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "text",
        "photo",
    )

    search_fields = ("=user__username",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "text",
        "photo",
    )

    search_fields = ("=user__username",)
