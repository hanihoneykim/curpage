# Generated by Django 4.1.7 on 2023-03-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tags", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Text",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성시간"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정됨")),
                (
                    "title",
                    models.CharField(default="", max_length=140, verbose_name="제목"),
                ),
                ("body", models.TextField(verbose_name="내용")),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="texts",
                        to="tags.tag",
                        verbose_name="태그",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
