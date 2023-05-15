from rest_framework import serializers
from .models import DmRoom, Dm
from users.serializers import TinyUserSerializer


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
    member = TinyUserSerializer(read_only=True)

    class Meta:
        model = Dm
        fields = ("message_txt",)

    def message_txt(self):
        return f"{self.member} : ${self.message}"
