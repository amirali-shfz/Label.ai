\copy label FROM './dataset_processing/prod_dataset/label.csv' WITH (FORMAT csv, HEADER);
\copy image FROM './dataset_processing/prod_dataset/image.csv' WITH (FORMAT csv, HEADER);
\copy classification(img_id, label_id, pre_classified) FROM './dataset_processing/prod_dataset/classification.csv' WITH (FORMAT csv, HEADER);
\copy member FROM './dataset_processing/prod_dataset/member.csv' WITH (FORMAT csv, HEADER);
\copy submission(class_id, member_id, correct_label) FROM './dataset_processing/prod_dataset/submission.csv' WITH (FORMAT csv, HEADER);

DELETE FROM label WHERE label_id not in (SELECT DISTINCT label_id FROM classification);
