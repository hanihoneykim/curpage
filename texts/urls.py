from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/comments", views.TextComments.as_view()),
    path("", views.Texts.as_view()),
    path("<int:pk>", views.TextDetail.as_view()),
    path("<int:text_pk>/comments/<int:comment_pk>", views.CommentDetail.as_view()),
    path("<int:pk>/likes", views.TextLikes.as_view()),
]
