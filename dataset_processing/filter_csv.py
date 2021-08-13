import pandas as pd
import os
import requests
import random

MAX_NUM_IMAGES = 5000
NUM_TEST_IMAGES = 100

assert os.environ["PYTHONHASHSEED"] == "1"
random.seed(1)

os.makedirs('./dataset_processing/csv/filtered/', exist_ok=True)

# Get the labels we want to use
print('Loading Data...')
labels  = pd.read_csv('./dataset_processing/csv/downloads/labels.csv')
images  = pd.read_csv('./dataset_processing/csv/downloads/images.csv')[['ImageID', 'OriginalURL', 'Thumbnail300KURL', 'Rotation']]
classes = pd.read_csv('./dataset_processing/csv/downloads/classifications.csv')[['ImageID','LabelName','Confidence']]

print('Renaming Columns...')
images = images.rename(columns={'Thumbnail300KURL': 'SmallURL'})

print('Re-mapping IDs...')
# Strip /m/ from label id
labels['ID'] = labels['ID'].str.lstrip('/m/')
classes['LabelName'] = classes['LabelName'].str.lstrip('/m/')

print('Getting Valid Labels...')
# Set of labels we want to use
label_ids = set(labels['ID'].values)

# Remove classifications with unused labels
print('Removing Redundant Classifications...')
classes = classes[classes['LabelName'].isin(label_ids)]

print('Reducing the set of images...')
# Set of images we want to use
img_ids = set(random.sample(set(classes['ImageID'].values), MAX_NUM_IMAGES))

bad_img_ids = set()
increment = len(img_ids)//100
for i, img_id in enumerate(img_ids):
    if i % increment == 0:
        print(f'\t{i//increment}% done')
    row = images.loc[images['ImageID'] == img_id]
    og_url = row.OriginalURL.item()
    if not requests.head(og_url).ok:
        bad_img_ids.add(img_id)
        print(f'\tRemoving {og_url}')
    elif isinstance(row.SmallURL.item(), str) and not requests.head(row.SmallURL.item()).ok:
        row.SmallURL = None

img_ids = img_ids.difference(bad_img_ids)
img_ids_test = set(list(img_ids)[:NUM_TEST_IMAGES])

print(f'\t{len(img_ids)} of {MAX_NUM_IMAGES} remaining')

print('Setting default rotation to 0')
images['Rotation'] = images['Rotation'].fillna(0).astype(int)

# Remove Images that have no labels
print('Removing Images from image and classification dataframes')
images_prod = images[images['ImageID'].isin(img_ids)]
images_test = images[images['ImageID'].isin(img_ids_test)]

classes_prod = classes[classes['ImageID'].isin(img_ids)]
classes_test = classes[classes['ImageID'].isin(img_ids_test)]

print('Serializing files...')
labels.to_csv('./dataset_processing/csv/filtered/labels.csv', index=False)

images_prod.to_csv('./dataset_processing/csv/filtered/images_prod.csv', index=False)
images_test.to_csv('./dataset_processing/csv/filtered/images_test.csv', index=False)

classes_prod.to_csv('./dataset_processing/csv/filtered/classifications_prod.csv', index=False)
classes_test.to_csv('./dataset_processing/csv/filtered/classifications_test.csv', index=False)
