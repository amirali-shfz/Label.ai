import requests
import os

os.makedirs('csv/labels/', exist_ok=True)
os.makedirs('csv/links/', exist_ok=True)

downloads = [
    {'path': 'csv/label-descriptions.csv', 'url': 'https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv'},
    {'path': 'csv/labels/test_og.csv', 'url': 'https://storage.googleapis.com/openimages/v5/test-annotations-machine-imagelabels.csv'},
    {'path': 'csv/links/test_og.csv', 'url': 'https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv'},
]

for val in downloads:
    req = requests.get(val['url'])
    url_content = req.content
    csv_file = open(val['path'], 'wb')

    csv_file.write(url_content)
    csv_file.close()


