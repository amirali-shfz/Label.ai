from django.db import models

from label_ai.images.models import Image
from label_ai.labels.models import Label

class Classification(models.Model):
    class_id = models.AutoField(primary_key=True)
    confidence = models.FloatField()
    true_count = models.IntegerField()
    false_count = models.IntegerField()
    pre_classified = models.BooleanField()
    iid = models.ForeignKey(Image, models.DO_NOTHING, db_column='iid')
    lid = models.ForeignKey(Label, models.DO_NOTHING, db_column='lid')

    class Meta:
        db_table = 'classification'

# \copy Classification(iid, lid, confidence, true_count, false_count, pre_classified) FROM 'classifications.csv' DELIMITER ',' CSV;
