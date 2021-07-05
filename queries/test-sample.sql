
-- Query 1
SELECT image.small_url, label.name
FROM classification, image, label, (SELECT img_id FROM image ORDER BY RANDOM() LIMIT 1) as a
WHERE a.img_id = image.img_id AND classification.label_id = label.label_id AND image.img_id = classification.img_id

-- Query 2
SELECT i.original_url
FROM classification as c, image as i, label as l
WHERE i.img_id = c.img_id 
	AND c.label_id = l.label_id
	AND c.pre_classified = True 
	AND l.name = `${req.label}` 
	AND c.confidence > 0.8;


-- Query 3
SELECT img_id, l.name
FROM classification as c, label as l 
WHERE confidence < 0.5 
	AND pre_classified = TRUE 
	AND c.label_id = l.label_id;

SELECT img_id, l.name
FROM classification as c, label as l 
WHERE confidence > 0.95 
	AND pre_classified = TRUE 
	AND c.label_id = l.label_id;


-- Query 4
SELECT *
FROM
(
	SELECT 	
		label_id, 
		(SUM(ABS(confidence))/COUNT(*)) as avg_conf, 
		SUM(true_count) as tc, 
		SUM(false_count) as fc 
	FROM classification
	GROUP BY label_id
) AS a
WHERE (a.avg_conf > 0.45 AND a.avg_conf < 0.55) OR a.tc + a.fc < 10;


-- Query 5
INSERT into image Values(10000, 'https://farm6.staticflickr.com/2300/2041178335_8fc60e09fe_o.jpg','https://c5.staticflickr.com/3/2300/2041178335_da4967c386_z.jpg?zz=1', 0);
INSERT INTO label VALUES(10000, 'window');
INSERT INTO classification VALUES(10001, 0,0,0, 't', 10000, 10000);


-- Additional Feature 1
    -- Select labelers who have at least 400 classifications
CREATE VIEW QualifiedUsers AS SELECT * FROM member WHERE member_id IN (SELECT member_id FROM submission GROUP BY member_id HAVING COUNT(*) > 400);

    -- Extract the best performing labeller
(SELECT name FROM QualifiedUsers) EXCEPT (SELECT u1.name FROM QualifiedUsers as u1, QualifiedUsers as u2 WHERE u1.Trust < u2.Trust);


-- Additional Feature 2
SELECT * FROM member WHERE username = 'testuser1' AND password = 'password123';
