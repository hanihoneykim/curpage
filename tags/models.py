from django.db import models


class Tag(models.Model):
    """Model Definition for Tags"""

    name = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tag"
        verbose_name = "태그"
        verbose_name_plural = "태그"
