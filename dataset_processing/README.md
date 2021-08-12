# Dataset Processing

## To Use
Navigate to the root directory (`dataset_processing/..`)
Get modules `python -m pip install -r dataset_processing/requirements.txt`

### Download CSV files
`python dataset_processing/download_csv.py`

### Filter the CSV files
`PYTHONHASHSEED=1 python dataset_processing/filter_csv.py`

### Generate the test and production dataset
`python dataset_processing/convert_to_db_format.py`
`python dataset_processing/generate_submission_data.py`

## Important Links
https://storage.googleapis.com/openimages/web/download.html

### Labels Used
[csv/label-descriptions.csv](https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv)

### Images Labels
[csv/labels/test_og.csv](https://storage.googleapis.com/openimages/v5/test-annotations-machine-imagelabels.csv)

### Image Links
[csv/links/test_og.csv](https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv)

