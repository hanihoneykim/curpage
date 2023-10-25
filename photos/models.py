from django.db import models
from common.models import CommonModel
from django.conf import settings


class Photo(CommonModel):
    """Model Definition for Photos"""

    title = models.CharField(
        max_length=225,
        default="",
        verbose_name="제목",
    )
    photo = models.URLField(
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
        default="",
        verbose_name="태그",
        related_name="photos",
    )
    # photo_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


"""
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # S3 버킷 내의 업로드 경로와 파일 이름을 기반으로 URL을 설정
        self.image_url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/photos/{self.photo.name}"
        self.save(update_fields=["image_url"])
"""
