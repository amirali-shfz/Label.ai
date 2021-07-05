-- Create Tables Script
-- label
CREATE TABLE IF NOT EXISTS Label
(
    label_id   text PRIMARY KEY,
    name       text NOT NULL
);

-- image
CREATE TABLE IF NOT EXISTS Image
(
    img_id         text PRIMARY KEY,
    original_url   text NOT NULL,
    small_url      text,
    rotation       integer NOT NULL
);

-- user
CREATE TABLE IF NOT EXISTS Member
(
    member_id  SERIAL PRIMARY KEY,
    username   text NOT NULL,
    password   text NOT NULL,
    trust      float NOT NULL,
    name       text NOT NULL
);

-- classification
CREATE TABLE IF NOT EXISTS Classification
(
    class_id       SERIAL PRIMARY KEY,
    confidence     float GENERATED ALWAYS AS (CASE WHEN true_count + false_count = 0 THEN 0 ELSE ((true_count + 1.9208) / (true_count + false_count) - 1.96 * SQRT(CAST ((true_count * false_count) / (true_count + false_count) + 0.9604 AS FLOAT)) / (true_count + false_count)) / (1 + 3.8416 / (true_count + false_count)) END) STORED,
    true_count     integer NOT NULL,
    false_count    integer NOT NULL,
    pre_classified boolean NOT NULL,
    img_id         text NOT NULL,
    label_id       text NOT NULL,
    CONSTRAINT fk_image FOREIGN KEY ( img_id ) REFERENCES Image ( img_id ),
    CONSTRAINT fk_label FOREIGN KEY ( label_id ) REFERENCES Label ( label_id )
);

-- submission
CREATE TABLE IF NOT EXISTS Submission
(
    submission_id  SERIAL PRIMARY KEY,
    correct_label  boolean NOT NULL,
    member_id      integer NOT NULL,
    class_id       integer NOT NULL,
    CONSTRAINT fk_member FOREIGN KEY ( member_id ) REFERENCES Member ( member_id ),
    CONSTRAINT fk_classification FOREIGN KEY ( class_id ) REFERENCES Classification ( class_id )
);

-- indices
CREATE INDEX ON Classification ( img_id );
CREATE INDEX ON Classification ( label_id );

CREATE INDEX ON Submission ( member_id );
CREATE INDEX ON Submission ( class_id );

-- views
CREATE OR REPLACE VIEW ImgLabel (img_id, url, label) AS
    SELECT img_id, original_url, name FROM classification NATURAL JOIN label NATURAL JOIN image;


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
