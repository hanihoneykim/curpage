from django.contrib import admin
from .models import DmRoom, Dm


@admin.register(Dm)
class DmAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "dmroom",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = ("=user__username",)


@admin.register(DmRoom)
class DmRoomAdmin(admin.ModelAdmin):
    pass
