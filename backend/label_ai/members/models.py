from django.db import models

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    trust = models.FloatField()
    name = models.TextField()

    class Meta:
        db_table = 'member'
