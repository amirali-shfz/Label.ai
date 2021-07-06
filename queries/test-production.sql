-- 1. Calculate Classification Confidence
-- The confidence of each classification is dependent on the submissions of each user, and the trust we have of each user. We are using the lower bound of the Wilson confidence interval using weighted votes as successes/failures to define the confidence of the classification. We also initialize the confidence with 5 positive and 5 negative votes. We express this feature as a view so that the confidence can be auto generated based on submissions.

CREATE OR REPLACE VIEW ClassificationView (
    class_id,
    img_id,
    label_id,
    pre_classified,
    confidence
) AS
SELECT
    class_id,
    img_id,
    label_id,
    pre_classified,
    CASE WHEN total_votes = 0 THEN 0 ELSE ((positive_votes + 1.9208) / total_votes - 1.96 * SQRT(CAST ((positive_votes * (total_votes-positive_votes)) / total_votes + 0.9604 AS FLOAT)) / (total_votes)) / (1 + 3.8416 / (total_votes)) END
FROM (
    SELECT
        class_id,
        img_id,
        label_id,
        pre_classified,
        COALESCE(positive_votes, 5) positive_votes,
        COALESCE(total_votes, 10) total_votes
    FROM
        classification NATURAL LEFT JOIN (
            SELECT
                class_id,
                5+SUM(CASE WHEN correct_label THEN trust ELSE 0 END) AS positive_votes,
                10+SUM(trust) as total_votes
            FROM
                submission NATURAL JOIN member GROUP BY class_id ORDER BY class_id
        ) as foo
    ) as classification_votes;

-- 2. Get Classifications Prompt - return Image, Labels and Classifications
-- To obtain user opinion towards an image labelling, users are given a list of images and their respective label to classify. The following query supplies a random list of (n) images and labels (as well as the classification id) which the user has not classified before and need classification to which Label.ai’s backend will send to the frontend.

SELECT original_url, img_id, class_id, label_id, name
FROM (UnConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label) as a
WHERE NOT EXISTS (
	SELECT * FROM Submission WHERE member_id = %s AND class_id = a.class_id
)
ORDER BY RANDOM()
LIMIT %s;

-- 3. Create Submission
-- When a user labels an image with an appropriate label, the database is updated by creating a submission entry in the submission table. A submission entry is created for every single image label that the user submits. Each submission entry in the submission table contains the correctlabel, memberid, classificationid. The submission table is used to analyze and detect trends within the user label submissions.

INSERT INTO submission(correct_label, member_id, class_id)
VALUES(<correctlabel>,<memberid>,<classificationid>)


-- 4. Get all images with a specific confirmed label
-- To make testing easier for labellers, we can provide them with the list of images that have been confirmed as being labelled with a certain label. For example, if a labeller does not know the word ‘Papaya’ we can provide a list of images correctly labelled as papaya. Additionally, this can make AI model testing easier for users, as users can query a list of images that matches a specific label. The return list of images has a very high confidence of that label.

SELECT original_url, img_id
FROM ConfirmedClassification NATURAL JOIN Image
WHERE label_id = %s
LIMIT %s;

-- 5. Find Mislabelled Images (SFW)
-- In the database, each picture to label classification is assigned a source of truth (valued True if the label corresponds to the picture and False otherwise). This source of truth is the perceived source of truth by the client when they have inputted the image into Label.ai initially. After verification, the client can see which images / associated labels that they have “under classified” or “incorrectly classified”. Under classified images are images which are missing labels that should of been there. For example, an image which has a car and a human but is only labelled human is an under classified image. Incorrectly classified images are images which is given an incorrecty label. For example, a picture with just a cat but is labelled as dog is an incorrectly classified image. 

-- The client will be able to see both “under classified” or “incorrectly classified” in their frontend portal. To fetch these images, our backend performs the following sql queries.

-- Under Classified
SELECT original_url, name, img_id, label_id
FROM ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label 
WHERE NOT pre_classified
LIMIT %s;

-- Incorrectly Classified
SELECT original_url, name, img_id, label_id
FROM MisClassification NATURAL JOIN Image NATURAL JOIN Label
WHERE pre_classified
LIMIT %s;

-- 6. Get image labels that have not been verified (i.e. potential extra labels for images)
-- To ensure that all label/pairs are consistently tested, Label.ai will occasionally query labels that need more verification from labellers. Labels that fit this category are labels which have an average confidence that is close to 0.23 (i.e. labellers are not sure if the label corresponds to the image) and labels that have a low total number of verifications from labellers. The following query will select these labels-image pairings, which will have a greater chance of appearing on future label-image pairing lists for labellers.

SELECT label_id, AVG(confidence) as average_conf
FROM ClassificationView
GROUP BY label_id HAVING AVG(confidence) > 0.15 AND AVG(confidence) < 0.7
LIMIT %s;

-- 7. Custom Addition of Picture/Classifications/Labels/Submissions
-- Users who want their datasets verified can also make requests to Label.ai for specific images to be added and the list of labels that they want the image to be verified against. These images will be stored in Label.ai’s db and will randomly appear on the lists of image-label pairs that the labellers need to verify.

INSERT INTO submission Values(0,'t', 3, 8);
INSERT into image Values(10000, 'https://farm6.staticflickr.com/2300/2041178335_8fc60e09fe_o.jpg','https://c5.staticflickr.com/3/2300/2041178335_da4967c386_z.jpg?zz=1', 0);
INSERT INTO label VALUES(10000, 'window');
INSERT INTO classification VALUES(10000004,'4d4b4f850df89aaf','015p6','t');
