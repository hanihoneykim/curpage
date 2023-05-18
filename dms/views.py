from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import DmRoom, Dm
from .serializers import DmRoomGetSerializer, DmRoomPostSerializer, DmSerailizer


class DmRooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    """def get(self, request):
        all_dmrooms = DmRoom.objects.all()
        serializer = DmRoomGetSerializer(
            all_dmrooms,
            many=True,
        )
        return Response(serializer.data)"""

    def get(self, request):
        hosted_dmrooms = request.user.hosted_dmrooms.all()
        joined_dmrooms = request.user.joined_dmrooms.all()

        user_dmrooms = (hosted_dmrooms | joined_dmrooms).distinct().order_by("-pk")

        # user_dmrooms = request.user.dmrooms.all()
        serializer = DmRoomGetSerializer(
            user_dmrooms,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = DmRoomPostSerializer(data=request.data)
        if serializer.is_valid():
            dmroom = serializer.save(
                host=request.user,
            )
            serializer = DmRoomPostSerializer(dmroom)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DmRoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return DmRoom.objects.get(pk=pk)
        except DmRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        dmroom = self.get_object(pk)
        serializer = DmRoomGetSerializer(
            dmroom,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        dmroom = self.get_object(pk)
        if dmroom.host != request.user:
            raise PermissionDenied
        serializer = DmRoomPostSerializer(
            dmroom,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            dmroom = serializer.save(
                host=request.user,
            )
            serializer = DmRoomPostSerializer(dmroom)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dmroom = self.get_object(pk)
        if dmroom.host != request.user:
            raise PermissionDenied
        dmroom.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Dms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return DmRoom.objects.get(pk=pk)
        except DmRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        dmroom = self.get_object(pk)
        serializer = DmSerailizer(
            dmroom.dms.all(),
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        dmroom = self.get_object(pk)
        serializer = DmSerailizer(
            data=request.data,
            # context={"dmroom": dmroom, "request": request},
        )
        if serializer.is_valid():
            members = [dmroom.host, *dmroom.members.all()]
            if request.user in members:
                dm = serializer.save(
                    member=request.user,
                    dmroom=self.get_object(pk),
                )
                serializer = DmSerailizer(dm)
                return Response(serializer.data)
            else:
                raise PermissionDenied
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
