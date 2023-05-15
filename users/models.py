from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    profile_photo = models.ImageField(blank=True, verbose_name="프로필사진")
    name = models.CharField(
        max_length=100,
        default="",
        help_text="사용하실 이름 혹은 별명을 입력해주세요",
        verbose_name="이름/별명",
    )
    username = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="ID",
        help_text="15자 이내로 만들어주세요. 영어 소문자, 특수문자 (_) 사용 가능.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        unique=True,
        default="",
        verbose_name="이메일",
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default="",
        verbose_name="성별",
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    dmrooms = models.ManyToManyField(
        "dms.DmRoom",
        related_name="user_dmrooms",
    )
