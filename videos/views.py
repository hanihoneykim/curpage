from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video
from tags.models import Tag
from .serializers import VideoListSerializer, VideoDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied


class VideoList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_videos = Video.objects.all()
        serializer = VideoListSerializer(
            all_videos,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoListSerializer(data=request.data)
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

            video = serializer.save(
                user=request.user,
                tags=tag_list,
            )
            serializer = VideoListSerializer(video)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class VideoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        video = self.get_object(pk)
        serializer = VideoDetailSerializer(
            video,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        video = self.get_object(pk)
        if video.user != request.user:
            raise PermissionDenied
        serializer = VideoDetailSerializer(
            video,
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
                    video.tags.clear()
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    if created:
                        tag_list.append(tag_obj)
                    else:
                        tag_list.append(tag_obj)
            video = serializer.save(
                user=request.user,
                tags=tag_list,
            )
            serializer = VideoDetailSerializer(video)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        video = self.get_object(pk)
        if video.user != request.user:
            raise PermissionDenied
        video.delete()
        return Response(status=HTTP_204_NO_CONTENT)
