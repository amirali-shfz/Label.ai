\copy label FROM './dataset_processing/csv/db_ready/label.csv' WITH (FORMAT csv, HEADER);
\copy image FROM './dataset_processing/csv/db_ready/image.csv' WITH (FORMAT csv, HEADER);
\copy classification(img_id, label_id, true_count, false_count, pre_classified) FROM './dataset_processing/csv/db_ready/classification.csv' WITH (FORMAT csv, HEADER);
