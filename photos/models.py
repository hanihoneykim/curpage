from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    """Model Definition for Photos"""

    title = models.CharField(
        max_length=140,
        default="",
        verbose_name="제목",
    )
    photo = models.ImageField(
        null=True,
        default="",
        verbose_name="사진파일",
    )
    description = models.TextField(
        blank=True,
        verbose_name="내용",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="photos",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        blank=True,
        verbose_name="태그",
        related_name="photos",
    )

    def __str__(self):
        return self.title
