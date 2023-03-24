from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "body",
        "total_likes",
    )

    list_filter = [
        ("created_at", DateRangeFilter),
    ]

    search_fields = (
        "title",
        "=user__username",
    )
