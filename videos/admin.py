from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
    )

    search_fields = (
        "title",
        "=user__username",
    )
