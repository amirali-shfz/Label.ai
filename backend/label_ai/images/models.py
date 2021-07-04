from django.db import models


class Image(models.Model):
    img_id = models.TextField(primary_key=True)
    original_url = models.TextField()
    small_url = models.TextField()
    rotation = models.IntegerField()

    class Meta:
        db_table = 'image'
