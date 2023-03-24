from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "photo_count",
    )

    search_fields = (
        "title",
        "=user__username",
    )
