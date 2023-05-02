from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Text
from tags.models import Tag
from .serializers import TextListSerializer, TextDetailSerializer


class Texts(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_texts = Text.objects.all()
        serializer = TextListSerializer(
            all_texts,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TextDetailSerializer(data=request.data)
        if serializer.is_valid():
            tags = request.data.get("tags")
            tag_list = []
            for tag in tags:
                if not tag:
                    continue
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                if created:
                    tag_list.append(tag_obj)
                else:
                    tag_list.append(tag_obj)

            text = serializer.save(
                user=request.user,
                tags=tag_list,
            )
            serializer = TextDetailSerializer(text)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
