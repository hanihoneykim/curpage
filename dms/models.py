from django.db import models
from common.models import CommonModel


class Dm(CommonModel):

    """Direct Message Model Definition"""

    message = models.TextField(
        verbose_name="메세지",
    )
    member = models.ForeignKey(
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
        return f"{self.member} says : {self.message}"

    class Meta:
        verbose_name = "Direct Message"
        ordering = ["-created_at"]


class DmRoom(CommonModel):

    """Direct Message Room Model Definition"""

    title = models.CharField(
        max_length=15,
        default="",
    )
    host = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="hosted_dmrooms",
    )
    members = models.ManyToManyField(
        "users.User",
        related_name="joined_dmrooms",
    )

    def __str__(self):
        return f"DmRoom : {self.title}"

    class Meta:
        verbose_name = "Chatting Room"
        ordering = ["-created_at"]
