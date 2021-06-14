import requests as req
import os
import random

os.makedirs('test_dataset/', exist_ok=True)


# Filter label descriptions
label_ids = set(['/m/0199g', '/m/01bl7v', '/m/01d40f', '/m/01g317', '/m/0271t', '/m/02dl1y', '/m/03bt1vf', '/m/05r655', '/m/07yv9', '/m/04yx4'])
label_name = {}
with open('csv/label-descriptions.csv', 'r') as input, open('test_dataset/labels.csv', 'w') as output:
    for line in input:
        id, name = line.rstrip().split(',')
        if id in label_ids:
            label_name[id] = name
            output.write(line)
            

# Filter classifications
image_to_labels = {}
with open('csv/labels/test_og.csv', 'r') as input:
    for line in input:
        image_id, _, label_id, _  = line.split(',') 
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
with open('csv/links/test_reduced.csv', 'r') as input, open('test_dataset/images.csv', 'w') as output:
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

