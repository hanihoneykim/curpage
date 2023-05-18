from rest_framework import serializers
from .models import DmRoom, Dm
from users.serializers import TinyUserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework import viewsets


class DmRoomGetSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    members = TinyUserSerializer(read_only=True, many=True)

    class Meta:
        model = DmRoom
        fields = (
            "pk",
            "title",
            "host",
            "members",
        )


class DmRoomPostSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    members = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = DmRoom
        fields = (
            "pk",
            "title",
            "host",
            "members",
        )

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        dmroom = super().create(validated_data)
        dmroom.members.set(members)
        return dmroom

    # members 받을 때 pk 값의 list로 받음 (ex. "members":[2,3])


class DmSerailizer(serializers.ModelSerializer):
    message_txt = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Dm
        fields = ("message_txt",)

    def get_message_txt(self, obj):
        if obj.member in obj.dmroom.members.all():
            sender = str(obj.member)
        else:
            sender = obj.dmroom.host.name
        return f"{sender} : {obj.message}"

    """def create(self, validated_data):
        dmroom = self.context["dmroom"]
        members = validated_data.pop("members", [])

        dm = Dm.objects.create(
            dmroom=dmroom,
            member=self.context["request"].user,
            message=validated_data,
        )
        members.append(dm.member)
        dm.member.add(*members)  # 여기서 add 메서드를 사용합니다.

        return dm"""
