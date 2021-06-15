from django.db import models

from label_ai.classifications.models import Classification
from label_ai.members.models import Member


class Submission(models.Model):
    sid = models.AutoField(primary_key=True)
    correct_label = models.BooleanField()
    mid = models.ForeignKey(Member, models.DO_NOTHING, db_column='mid')
    cid = models.ForeignKey(Classification, models.DO_NOTHING, db_column='cid')

    class Meta:
        db_table = 'submission'
