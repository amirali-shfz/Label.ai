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
CREATE OR REPLACE VIEW img_label (img_id, url, label) AS SELECT original_url, NAME FROM classification NATURAL JOIN label NATURAL JOIN image;
