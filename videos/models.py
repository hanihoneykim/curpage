from django.db import models
from common.models import CommonModel


class Video(CommonModel):

    """Video Model Definition"""

    title = models.CharField(
        max_length=140,
        default="",
        verbose_name="제목",
    )
    video = models.URLField()
    description = models.TextField(
        blank=True,
        verbose_name="내용",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="videos",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        blank=True,
        verbose_name="태그",
        related_name="videos",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
