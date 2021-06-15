import pandas as pd
import os

os.makedirs('csv/filtered/', exist_ok=True)

# Get the labels we want to use
labels  = pd.read_csv('csv/downloads/labels.csv')
images  = pd.read_csv('csv/downloads/images.csv')[['ImageID', 'OriginalURL', 'Thumbnail300KURL', 'Rotation']]
classes = pd.read_csv('csv/downloads/classifications.csv')[['ImageID','LabelName','Confidence']]

# Strip /m/ from label id
labels['ID'] = labels['ID'].str.lstrip('/m/')
classes['LabelName'] = classes['LabelName'].str.lstrip('/m/')

images['Rotation'] = images['Rotation'].fillna(0).astype(int)

# Set of labels we want to use
label_ids = set(labels['ID'].values)

# Remove classifications with unused labels
classes = classes[classes['LabelName'].isin(label_ids)]

# Set of images we want to use
img_ids = set(classes['ImageID'].values)

# Remove Images that have no labels
images = images[images['ImageID'].isin(img_ids)]

labels.to_csv('csv/filtered/labels.csv', index=False)
images.to_csv('csv/filtered/images.csv', index=False)
classes.to_csv('csv/filtered/classifications.csv', index=False)
