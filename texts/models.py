from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from common.models import CommonModel
from comments.models import Like


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
        default="",
        verbose_name="태그",
        related_name="texts",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(text):
        return text.title

    def total_likes(self):
        return self.likes.filter(like=True).count()

    def comments_count(text):
        return text.comments.count()
