import pandas as pd
from shutil import copyfile

import random

random.seed(1)

copyfile('./dataset_processing/csv/filtered/images_prod.csv', './dataset_processing/prod_dataset/image.csv')
copyfile('./dataset_processing/csv/filtered/images_test.csv', './dataset_processing/test_dataset/image.csv')

copyfile('./dataset_processing/csv/filtered/labels.csv', './dataset_processing/test_dataset/label.csv')
copyfile('./dataset_processing/csv/filtered/labels.csv', './dataset_processing/prod_dataset/label.csv')

def calc_preclassified(row):
    return random.uniform(0, 1) > 0.05

classes_prod = pd.read_csv('./dataset_processing/csv/filtered/classifications_prod.csv')
classes_test = pd.read_csv('./dataset_processing/csv/filtered/classifications_test.csv')

classes_prod['PreClassified'] = classes_prod.apply(calc_preclassified, axis=1)
classes_test['PreClassified'] = classes_test.apply(calc_preclassified, axis=1)

classes_prod[['ImageID','LabelName','PreClassified']].to_csv('./dataset_processing/prod_dataset/classification.csv', index=False)
classes_test[['ImageID','LabelName','PreClassified']].to_csv('./dataset_processing/test_dataset/classification.csv', index=False)
