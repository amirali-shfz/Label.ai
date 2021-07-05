from django.db import models

from label_ai.images.models import Image
from label_ai.labels.models import Label


class Classification(models.Model):
    cid = models.AutoField(primary_key=True)
    confidence = models.FloatField()
    true_count = models.IntegerField()
    false_count = models.IntegerField()
    pre_classified = models.BooleanField()
    img_id = models.ForeignKey(Image, models.DO_NOTHING, db_column='img_id')
    label_id = models.ForeignKey(Label, models.DO_NOTHING, db_column='label_id')

    class Meta:
        db_table = 'classification'

# \copy Classification(iid, lid, confidence, true_count, false_count, pre_classified) FROM 'classifications.csv' DELIMITER ',' CSV;
