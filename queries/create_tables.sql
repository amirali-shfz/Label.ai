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
    img_id         text NOT NULL,
    label_id       text NOT NULL,
    pre_classified boolean NOT NULL,
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
