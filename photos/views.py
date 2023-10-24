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
import boto3


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
            # 이미 좋아요를 누른 경우
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=HTTP_400_BAD_REQUEST)

        # 서버 응답에 업데이트된 좋아요 카운트와 is_like 값을 포함
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


class S3Uploads(APIView):
    def post(self, request):
        try:
            photo = request.FILES.get("photo")
            user = request.data.get("user")
            tags = request.data.get("tags")
            title = request.data.get("title")
            description = request.data.get("description")

            s3r = boto3.resource(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            key = "%s/%s" % (user, photo.name)

            s3r.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=key, Body=photo, ContentType="image/jpeg"
            )
            image_url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{key}"

            photo = Photo.objects.create(
                title=title,
                description=description,
                user=user,
                image_url=image_url,
                tags=tags,
            )

            # 처리 완료 후 응답
            return Response({"MESSAGE": "SUCCESS"}, status=HTTP_200_OK)

        except Exception as e:
            return Response({"ERROR": str(e)}, status=HTTP_400_BAD_REQUEST)
