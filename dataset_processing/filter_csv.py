import pandas as pd

# Filter Columns
pd.read_csv('csv/links/test_og.csv')[['ImageID', 'OriginalURL', 'Thumbnail300KURL', 'Rotation']].to_csv('csv/links/test_col-filtered.csv', index=False)

# Get the labels we want to use
label_ids = set()
with open('csv/label-descriptions.csv', 'r') as input:
    for line in input:
        label_ids.add(line[:line.find(',')])

# Remove labels we don't want to use
image_ids = set()
with open('csv/labels/test_og.csv', 'r') as input, open('csv/links/test_reduced.csv', 'w') as output:
    for line in input:
        image_id, _, label_id, _  = line.split(',') 
        if label_id in label_ids:
            output.write(line)
            image_ids.add(image_id)

# Remove images with no labels
with open('csv/links/test_col-filtered.csv', 'r') as input, open('csv/links/test_reduced.csv', 'w') as output:
    output.writelines([line for line in input if line[:line.find(',')] in image_ids])
    