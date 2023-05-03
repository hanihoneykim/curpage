from django.urls import path
from . import views

urlpatterns = [
    path("", views.Tags.as_view()),
    # path("<int:pk>", views.TextDetail.as_view()),
]
