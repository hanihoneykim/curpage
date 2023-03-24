from django.contrib import admin
from .models import Comment, Like


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
        "video",
    )

    search_fields = (
        "=user__username",
        "photo__title__icontains",
        "text__title__icontains",
        "video__title__icontains",
    )
