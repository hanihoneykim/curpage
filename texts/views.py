from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Text
from tags.models import Tag
from comments.models import Comment, Like
from .serializers import TextListSerializer, TextDetailSerializer
from comments.serializers import CommentSerializer, LikeSerializer


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


class TextDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Text.objects.get(pk=pk)
        except Text.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        text = self.get_object(pk)
        serializer = TextDetailSerializer(
            text,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        text = self.get_object(pk)
        if text.user != request.user:
            raise PermissionDenied
        serializer = TextDetailSerializer(
            text,
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
                    text.tags.clear()
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

    def delete(self, request, pk):
        text = self.get_object(pk)
        if text.user != request.user:
            raise PermissionDenied
        text.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TextComments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Text.objects.get(pk=pk)
        except Text.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        text = self.get_object(pk)
        serializer = CommentSerializer(
            text.comments.all(),
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(
                user=request.user,
                text=self.get_object(pk),
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data)


class CommentDetail(APIView):
    def get(self, request, text_pk, comment_pk):
        text = Text.objects.get(pk=text_pk)
        comment = Comment.objects.get(pk=comment_pk, text=text)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, text_pk, comment_pk):
        text = Text.objects.get(pk=text_pk)
        comment = Comment.objects.get(pk=comment_pk, text=text)
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TextLikes(APIView):
    def get_object(self, pk):
        try:
            return Text.objects.get(pk=pk)
        except Text.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        text = self.get_object(pk)
        likes = text.likes.filter(like=True)
        serializer = LikeSerializer(
            likes,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        text = self.get_object(pk)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            like = serializer.save(
                like=True,
                user=request.user,
                text=text,
            )
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        text = self.get_object(pk)
        like = text.likes.filter(user=request.user).first()
        like.delete()
        return Response(status=HTTP_204_NO_CONTENT)
