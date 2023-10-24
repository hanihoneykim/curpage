from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from .models import Photo
from tags.models import Tag
from comments.models import Like
from comments.serializers import LikeSerializer
from .serializers import PhotoListSerializer, PhotoDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
)
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.generics import RetrieveAPIView
import requests


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
            tags_str = request.data.get("tags")
            tag_list = [tag.strip() for tag in tags_str.split(",")]
            tag_objects = []
            for tag_name in tag_list:
                if not tag_name:
                    continue
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                if created:
                    tag_objects.append(tag_obj)
                else:
                    tag_objects.append(tag_obj)

            photo = serializer.save(
                user=request.user,
            )
            photo.tags.set(tag_objects)
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
            context={"request": request},
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
            context={"request": request},
        )
        if serializer.is_valid():
            tags_str = request.data.get("tags")
            tag_list = [tag.strip() for tag in tags_str.split(",")]
            tag_objects = []
            for tag_name in tag_list:
                if not tag_name:
                    continue
                # 기존 태그를 모두 삭제합니다
                photo.tags.clear()
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                if created:
                    tag_objects.append(tag_obj)
                else:
                    tag_objects.append(tag_obj)
            photo = serializer.save(
                user=request.user,
            )
            photo.tags.set(tag_objects)
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


class PhotoLikes(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        photo = self.get_object(pk)
        likes = photo.likes.filter(like=True)
        serializer = LikeSerializer(
            likes,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request, pk):
        photo = self.get_object(pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            photo=photo,
            defaults={"like": True},
        )
        if not created:
            # 이미 좋아요를 누른 경우.
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=HTTP_400_BAD_REQUEST)

        # 서버 응답에 업데이트된 좋아요 카운트와 is_like 값을 포함.
        serializer = LikeSerializer(like)
        return Response(
            {
                "count_likes": photo.likes.filter(like=True).count(),
                "is_like": True,
                # 기타 필요한 데이터도 반환할 수 있음.
            }
        )

    def delete(self, request, pk):
        photo = self.get_object(pk)
        like = photo.likes.filter(user=request.user).first()
        if like:
            # 사용자 객체간의 동등성을 확인하여 좋아요 삭제
            if like.user == request.user:
                like.delete()
                # 서버 응답에 업데이트된 좋아요 카운트와 is_like 값을 포함
                return Response(
                    {
                        "count_likes": photo.likes.filter(like=True).count(),
                        "is_like": False,
                        # 기타 필요한 데이터도 반환할 수 있음
                    }
                )
            else:
                # 현재 사용자와 좋아요를 누른 사용자가 다른 경우
                return Response({"detail": "삭제 권한이 없습니다."}, status=HTTP_403_FORBIDDEN)
        else:
            # 이미 좋아요가 취소된 경우
            return Response({"detail": "이미 좋아요를 취소했습니다."}, status=HTTP_400_BAD_REQUEST)


class GetUploadURL(APIView):
    def post(self):
        url = (
            f"https://api.cloudflare.com/client/v4/accounts{settings.CF_ID}/images/v2/direct_upload"
        )
        one_time_url = requests.post(url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"})
        one_time_url = one_time_url.json()
        result = one_time_url("result")
        return Response({"uploadURL": result.get("uploadURL")})
