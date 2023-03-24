from django.db import models
from common.models import CommonModel


class Dm(CommonModel):

    """Direct Message Model Definition"""

    message = models.TextField(
        verbose_name="메세지",
    )
    user = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="dms",
    )
    dmroom = models.ForeignKey(
        "dms.DmRoom",
        on_delete=models.CASCADE,
        related_name="dms",
    )

    def __str__(self):
        return f"{self.user} says : {self.message}"

    class Meta:
        verbose_name = "Direct Message"


class DmRoom(CommonModel):

    """Direct Message Room Model Definition"""

    users = models.ManyToManyField("users.User")

    def __str__(self):
        return "DmRoom"

    class Meta:
        verbose_name = "Chatting Room"
