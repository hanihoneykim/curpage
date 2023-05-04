from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from tags.models import Tag
from .serializers import PhotoListSerializer, PhotoDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied


class PhotoList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_photos = Photo.objects.all()
        serializer = PhotoListSerializer(
            all_photos,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PhotoListSerializer(data=request.data)
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

            photo = serializer.save(
                user=request.user,
                tags=tag_list,
            )
            serializer = PhotoListSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        photo = self.get_object(pk)
        serializer = PhotoDetailSerializer(
            photo,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        photo = self.get_object(pk)
        if photo.user != request.user:
            raise PermissionDenied
        serializer = PhotoDetailSerializer(
            photo,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            tags = request.data.get("tags")
            tag_list = []
            for tag in tags:
                if not tag:
                    continue
                elif tag:
                    photo.tags.clear()
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    if created:
                        tag_list.append(tag_obj)
                    else:
                        tag_list.append(tag_obj)
            photo = serializer.save(
                user=request.user,
                tags=tag_list,
            )
            serializer = PhotoDetailSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.user != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
