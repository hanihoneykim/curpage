from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Tag
from .serializers import TagListSerializer


class Tags(APIView):
    def get(self, request):
        all_tags = Tag.objects.all()
        serializer = TagListSerializer(
            all_tags,
            many=True,
        )
        return Response(serializer.data)
