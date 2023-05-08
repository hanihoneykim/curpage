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
    list_display = ("__str__",)

    search_fields = ("=user__username",)
