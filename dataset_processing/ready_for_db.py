import pandas as pd
from shutil import copyfile

import random

random.seed(1)

copyfile('./csv/filtered/images.csv', './csv/db_ready/image.csv')
copyfile('./csv/filtered/labels.csv', './csv/db_ready/label.csv')

def calc_preclassified(row):
    return random.uniform(0, 1) > 0.05

def calc_total_votes(row):
    # return max(30, int(400*row.Confidence + random.gauss(0, 50)))
    return 0

def calc_positive_votes(row):
    # return int(min(0.98, random.gauss(row.Confidence, 0.01)) * row.TotalCount)
    return 0

classes = pd.read_csv('./csv/filtered/classifications.csv')
classes['TotalCount'] = classes.apply(calc_total_votes, axis=1)
classes['TrueCount'] = classes.apply(calc_positive_votes, axis=1)
classes['FalseCount'] = classes.TotalCount - classes.TrueCount
classes['PreClassified'] = classes.apply(calc_preclassified, axis=1)

classes = classes[['ImageID','LabelName','TrueCount','FalseCount','PreClassified']]

classes.to_csv('csv/db_ready/classification.csv', index=False)
