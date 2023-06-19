from rest_framework.views import APIView
from rest_framework.response import Response
from photos.models import Photo
from texts.models import Text
from videos.models import Video
from .serializers import HomeSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied


class Home(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        latest_photos = Photo.objects.order_by("-created_at")[:12]
        latest_texts = Text.objects.order_by("-created_at")[:7]
        latest_videos = Video.objects.order_by("-created_at")[:7]
        serializer = HomeSerializer(
            {
                "photos": latest_photos,
                "videos": latest_videos,
                "texts": latest_texts,
            }
        )
        return Response(serializer.data)
