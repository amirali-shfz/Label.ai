from django.db import models


class Label(models.Model):
    lid = models.TextField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'label'

