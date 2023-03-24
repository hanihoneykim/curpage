from django.db import models
from common.models import CommonModel


class Text(CommonModel):
    """Model Definition for Texts"""

    title = models.CharField(
        max_length=140,
        default="",
        verbose_name="제목",
    )
    body = models.TextField(
        verbose_name="내용",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="texts",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        blank=True,
        verbose_name="태그",
        related_name="texts",
    )

    def __str__(text):
        return text.title

    def total_likes(text):
        return text.likes.count()
