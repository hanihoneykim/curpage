# Generated by Django 4.1.7 on 2023-03-24 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comments", "0003_initial"),
        ("texts", "0001_initial"),
        ("videos", "0001_initial"),
        ("photos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="videos.video",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="photo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="photos.photo",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="text",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="texts.text",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="videos.video",
            ),
        ),
    ]
