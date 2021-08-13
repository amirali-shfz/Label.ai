
-- Contains each the image id, url and label for each classification
CREATE OR REPLACE VIEW ImgLabel (img_id, url, label) AS
    SELECT img_id, original_url, name FROM classification NATURAL JOIN label NATURAL JOIN image;


-- The View for all application querying of classifications
--      It calculates the lowerbound of the wilson confidence interval of a positive classification
--      the accumulated trust of positive submissions as 'positive votes' and accumulated trust of all
--      submissions as total trust.
CREATE OR REPLACE VIEW ClassificationView (
    class_id,
    img_id,
    label_id,
    pre_classified,
    total_votes,
    confidence
) AS
SELECT
    class_id,
    img_id,
    label_id,
    pre_classified,
    total_votes,
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


-- All the classifications which we consider to be incorrect
CREATE OR REPLACE VIEW Misclassification (
    class_id,
    img_id,
    label_id,
    pre_classified,
    total_votes,
    confidence
) AS
SELECT *
FROM ClassificationView
WHERE confidence < 0.08;


-- All the classifications which we consider to be correct
CREATE OR REPLACE VIEW ConfirmedClassification (
    class_id,
    img_id,
    label_id,
    pre_classified,
    total_votes,
    confidence
) AS
SELECT * FROM
ClassificationView
WHERE confidence >= 0.90;


-- All the classifications which need more submissions in order to confirm or discredit
CREATE OR REPLACE VIEW UnconfirmedClassification (
    class_id,
    img_id,
    label_id,
    pre_classified,
    total_votes,
    confidence
) AS
SELECT *
FROM ClassificationView
WHERE confidence >= 0.08 OR confidence < 0.90;