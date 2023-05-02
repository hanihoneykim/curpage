from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.TagViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.TagViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
