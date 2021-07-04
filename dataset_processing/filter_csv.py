import pandas as pd
import os
import requests
import random

from requests.api import request

MAX_NUM_IMAGES = 5000

random.seed(1)
os.makedirs('csv/filtered/', exist_ok=True)

# Get the labels we want to use
print('Loading Data...')
labels  = pd.read_csv('csv/downloads/labels.csv')
images  = pd.read_csv('csv/downloads/images.csv')[['ImageID', 'OriginalURL', 'Thumbnail300KURL', 'Rotation']]
classes = pd.read_csv('csv/downloads/classifications.csv')[['ImageID','LabelName','Confidence']]

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
img_ids = set(classes['ImageID'].values)
img_ids = set(random.sample(img_ids, MAX_NUM_IMAGES))

for index, row in images.iterrows():
    img_id = row['ImageID']
    og_url = row['OriginalURL']
    small_url = row['SmallURL']
    if img_id in img_ids:
        if not requests.get(og_url).ok:
            img_ids.remove(row['ImageID'])
            print(f'\t({(index+1)*100/len(images):.2f}% done)... Removing {og_url}')
print(f'\t{len(img_ids)} of {MAX_NUM_IMAGES} remaining')

# Remove Images that have no labels
print('Removing Images from image and classification dataframes')
images = images[images['ImageID'].isin(img_ids)]
classes = classes[classes['ImageID'].isin(img_ids)]

print('Setting default rotation to 0')
images['Rotation'] = images['Rotation'].fillna(0).astype(int)

print('Serializing files...')
labels.to_csv('csv/filtered/labels.csv', index=False)
images.to_csv('csv/filtered/images.csv', index=False)
classes.to_csv('csv/filtered/classifications.csv', index=False)
