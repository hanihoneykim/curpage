from django.urls import path
from . import views

urlpatterns = [
    path("", views.DmRooms.as_view()),
    path("<int:pk>", views.DmRoomDetail.as_view()),
    # path("<int:pk>/dms", views.Dms.as_view()),
]
