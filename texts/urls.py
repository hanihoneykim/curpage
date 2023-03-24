from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_texts),
    path("<int:text_pk>", views.see_one_text),
]
