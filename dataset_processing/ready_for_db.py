import pandas as pd
from shutil import copyfile

import random

random.seed(1)

copyfile('./csv/filtered/images.csv', './csv/db_ready/image.csv')
copyfile('./csv/filtered/labels.csv', './csv/db_ready/label.csv')

def calc_preclassified(row):
    return random.uniform(0, 1) > 0.05

classes = pd.read_csv('./csv/filtered/classifications.csv')
classes['PreClassified'] = classes.apply(calc_preclassified, axis=1)

classes = classes[['ImageID','LabelName','PreClassified']]

classes.to_csv('csv/db_ready/classification.csv', index=False)
