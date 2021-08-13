\copy label FROM './dataset_processing/test_dataset/label.csv' WITH (FORMAT csv, HEADER);
\copy image FROM './dataset_processing/test_dataset/image.csv' WITH (FORMAT csv, HEADER);
\copy classification(img_id, label_id, pre_classified) FROM './dataset_processing/test_dataset/classification.csv' WITH (FORMAT csv, HEADER);
DELETE FROM label WHERE label_id not in (SELECT DISTINCT label_id FROM classification);


INSERT INTO member(member_id,username, password, trust, name, is_admin) VALUES
    (1,'admin','123',1,'adminname',TRUE),
    (2,'jacobk52','12345',100,'jacobkim',FALSE),
    (3,'wbhildeb', '1092745', 5, 'Walker',FALSE),
    (4,'kfeng', '1289501', 10, 'Kevin',FALSE),
    (5,'no_trust', '12380', 0, 'TrollMan42069',FALSE);

INSERT INTO submission(class_id, member_id, correct_label) VALUES
    (3, 1, False), (2, 2, False), (12, 1, False), (14, 2, False), (9, 3, True), (10, 2, True), (1, 3, True), (3, 1, True), (1, 1, False), (7, 3, False), (14, 2, False), (11, 1, True), (5, 2, True), (7, 2, True), (4, 2, True), (6, 3, True), (14, 3, True), (13, 2, True), (9, 3, True), (11, 3, False), (12, 1, False), (11, 1, False), (8, 3, True), (8, 2, True), (13, 2, True), (8, 2, False), (7, 1, True), (13, 3, False), (10, 3, False), (4, 3, True);