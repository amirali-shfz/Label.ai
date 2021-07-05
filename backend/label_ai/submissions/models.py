from django.db import models

from label_ai.classifications.models import Classification
from label_ai.members.models import Member


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    correct_label = models.BooleanField()
    member_id = models.ForeignKey(Member, models.DO_NOTHING, db_column='member_id')
    class_id = models.ForeignKey(Classification, models.DO_NOTHING, db_column='class_id')

    class Meta:
        db_table = 'submission'
