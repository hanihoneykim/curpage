from django.db import models
from common.models import CommonModel


class Comment(CommonModel):

    """Comment Model Definition"""

    comment = models.TextField(
        verbose_name="댓글",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    text = models.ForeignKey(
        "texts.Text",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    photo = models.ForeignKey(
        "photos.Photo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    video = models.ForeignKey(
        "videos.Video",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user}'s comment"


class Like(models.Model):

    """Like Model Definition"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    text = models.ForeignKey(
        "texts.Text",
        on_delete=models.CASCADE,
        related_name="likes",
        blank=True,
        null=True,
    )
    photo = models.ForeignKey(
        "photos.Photo",
        on_delete=models.CASCADE,
        related_name="likes",
        blank=True,
        null=True,
    )
    video = models.ForeignKey(
        "videos.Video",
        on_delete=models.CASCADE,
        related_name="likes",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user} likes ♥︎"
