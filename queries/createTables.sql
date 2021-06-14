-- Create Tables Script
-- label
CREATE TABLE IF NOT EXISTS Label
(
 lid  uuid NOT NULL,
 name string NOT NULL,
 CONSTRAINT PK_label PRIMARY KEY ( lid )
);

-- photo
CREATE TABLE IF NOT EXISTS Photo
(
 pid          text NOT NULL,
 original_url text NOT NULL,
 small_url    text NOT NULL,
 rotation     int NOT NULL,
 CONSTRAINT PK_photo PRIMARY KEY ( pid )
);

-- user
CREATE TABLE IF NOT EXISTS "User"
(
 uid      uuid NOT NULL,
 username text NOT NULL,
 password text NOT NULL,
 trust    float NOT NULL,
 name     text NOT NULL,
 CONSTRAINT PK_user PRIMARY KEY ( uid )
);

-- classification
CREATE TABLE IF NOT EXISTS Classification
(
 cid            uuid NOT NULL,
 photo_id       uuid NOT NULL,
 label          uuid NOT NULL,
 confidence     float NOT NULL,
 true_count     int NOT NULL,
 false_count    int NOT NULL,
 pre_classified boolean NOT NULL,
 pid            text NOT NULL,
 lid            uuid NOT NULL,
 CONSTRAINT PK_classification PRIMARY KEY ( cid ),
 CONSTRAINT FK_39 FOREIGN KEY ( pid ) REFERENCES Photo ( pid ),
 CONSTRAINT FK_45 FOREIGN KEY ( lid ) REFERENCES Label ( lid )
);

-- submission
CREATE TABLE IF NOT EXISTS Submission
(
 sid           uuid NOT NULL,
 correct_label boolean NOT NULL,
 uid           uuid NOT NULL,
 cid           uuid NOT NULL,
 CONSTRAINT PK_userclassification PRIMARY KEY ( sid ),
 CONSTRAINT FK_48 FOREIGN KEY ( uid ) REFERENCES "User" ( uid ),
 CONSTRAINT FK_51 FOREIGN KEY ( cid ) REFERENCES Classification ( cid )
);

-- index
CREATE INDEX fkIdx_40 ON Classification
(
 pid
);

CREATE INDEX fkIdx_46 ON Classification
(
 lid
);

CREATE INDEX fkIdx_49 ON Submission
(
 uid
);

CREATE INDEX fkIdx_52 ON Submission
(
 cid
);
