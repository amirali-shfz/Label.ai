import requests as req
import os

os.makedirs('test_dataset/')


# Filter label descriptions
label_ids = set(['/m/0199g', '/m/015qbp', '/m/015qff', '/m/01940j', '/m/01bfm9', '/m/01bl7v', '/m/01d40f', '/m/01g317', '/m/0271t', '/m/02dgv', '/m/02crq1', '/m/02dl1y', '/m/03bt1vf', '/m/05r655', '/m/07yv9', '/m/04yx4'])
with open('csv/label-descriptions.csv', 'r') as input, open('test_dataset/label-descriptions.csv', 'w') as output:
    output.writelines([line for line in input if line[:line.find(',')] in label_ids])

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


image_ids = set()
for image_id, labels in image_to_labels.items():
    if len(labels) > 4:
        image_ids.add(image_id)

    if len(image_ids) == 25:
        break

# Filter links
with open('csv/links/test_reduced.csv', 'r') as input, open('test_dataset/links.csv', 'w') as output:
    for line in input:
        img_id,img_url,_,_ = line.split(',')
        if img_id in image_ids:
            if req.get(img_url).ok:
                output.writelines(line)
            else:
                image_ids.remove(img_id)

with open('test_dataset/labels.csv', 'w') as output:    
    for img_id in image_ids:
        img_labels = image_to_labels[img_id]
        for label_id in label_ids:
            output.write(','.join([img_id, label_id, '0,0,0', ('T' if label_id in img_labels else 'F')])+ '\n')


