from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Comment
from comments.serializers import CommentSerializer


class CommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(
            comment,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment.user != request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
