import requests as req
import pandas as pd
import os
import random

os.makedirs('test_dataset/', exist_ok=True)


# Filter label descriptions
label_ids = set(['0199g', '01bl7v', '01d40f', '01g317', '0271t', '02dl1y', '03bt1vf', '05r655', '07yv9', '04yx4'])

labels = pd.read_csv('csv/filtered/labels.csv')
images = pd.read_csv('csv/filtered/images.csv')
classes = pd.read_csv('csv/filtered/classifications.csv')

label_name = labels.set_index(labels.ID).to_dict()['Name']

## Get most used labels
# most_classed = classes.groupby('LabelName').count().sort_values('ImageID', ascending=False)
# most_classed['Label'] = most_classed.index.map(label_name)
# most_classed.rename({'ImageID':'Frequency'}).set_index('Label')[['Frequency']].to_csv('classification_frequency.csv')

labels = labels[labels['ID'].isin(label_ids)]

# Filter classifications
image_to_labels = {}
with open('csv/filtered/classifications.csv', 'r') as input:
    for line in input:
        image_id, label_id, _  = line.split(',') 
        if label_id in label_ids:
            if image_id in image_to_labels:
                image_to_labels[image_id].add(label_id)
            else:
                image_to_labels[image_id] = set([label_id])

random.seed('not sexy')

image_to_labels = dict(filter(lambda kvp: len(kvp[1]) > 3, image_to_labels.items()))
img_ids = list(image_to_labels.keys())
random.shuffle(img_ids)
img_ids = img_ids[:50]

# Filter links
with open('csv/filtered/images.csv', 'r') as input, open('test_dataset/images.csv', 'w') as output:
    for line in input:
        img_id,img_url,_,_ = line.split(',')
        if img_id in img_ids:
            if req.get(img_url).ok:
                output.write(line)
            else:
                img_ids.remove(img_id)


label_occurrences = dict.fromkeys(label_ids, 0)
with open('test_dataset/classifications.csv', 'w') as output:    
    for img_id in img_ids:
        img_labels = image_to_labels[img_id]
        for label_id in label_ids:
            classified = label_id in img_labels
            if random.uniform(0, 1) < 1/100:
                classified = not classified

            if classified:
                label_occurrences[label_id] += 1
            output.write(','.join([img_id, label_id, '0,0,0', ('T' if classified else 'F')])+ '\n')

for id in label_ids:
    print(f'{label_occurrences[id]} occurrences of {label_name[id]} ({id})')


labels.to_csv('test_dataset/labels.csv', index=False)
# images.to_csv('test_dataset/images.csv', index=False)
# classes.to_csv('test_dataset/classifications.csv', index=False)
