from django.db import models


class Label(models.Model):
    label_id = models.TextField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'label'

