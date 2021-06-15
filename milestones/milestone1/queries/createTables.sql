-- Create Tables Script
-- label
CREATE TABLE IF NOT EXISTS Label
(
 lid  text NOT NULL,
 name text NOT NULL,
 CONSTRAINT PK_label PRIMARY KEY ( lid )
);

-- image
CREATE TABLE IF NOT EXISTS Image
(
 iid          text NOT NULL,
 original_url text NOT NULL,
 small_url    text NOT NULL,
 rotation     integer NOT NULL,
 CONSTRAINT PK_photo PRIMARY KEY ( iid )
);

-- user
CREATE TABLE IF NOT EXISTS Member
(
 mid      serial NOT NULL,
 username text NOT NULL,
 password text NOT NULL,
 trust    float NOT NULL,
 name     text NOT NULL,
 CONSTRAINT PK_user PRIMARY KEY ( mid )
);

-- classification
CREATE TABLE IF NOT EXISTS Classification
(
 cid            serial NOT NULL,
 confidence     float NOT NULL,
 true_count     integer NOT NULL,
 false_count    integer NOT NULL,
 pre_classified boolean NOT NULL,
 iid            text NOT NULL,
 lid            text NOT NULL,
 CONSTRAINT PK_classification PRIMARY KEY ( cid ),
 CONSTRAINT FK_39 FOREIGN KEY ( iid ) REFERENCES Image ( iid ),
 CONSTRAINT FK_45 FOREIGN KEY ( lid ) REFERENCES Label ( lid )
);

-- submission
CREATE TABLE IF NOT EXISTS Submission
(
 sid           serial NOT NULL,
 correct_label boolean NOT NULL,
 mid           integer NOT NULL,
 cid           integer NOT NULL,
 CONSTRAINT PK_userclassification PRIMARY KEY ( sid ),
 CONSTRAINT FK_48 FOREIGN KEY ( mid ) REFERENCES Member ( mid ),
 CONSTRAINT FK_51 FOREIGN KEY ( cid ) REFERENCES Classification ( cid )
);

-- index
CREATE INDEX fkIdx_40 ON Classification
(
 iid
);

CREATE INDEX fkIdx_46 ON Classification
(
 lid
);

CREATE INDEX fkIdx_49 ON Submission
(
 mid
);

CREATE INDEX fkIdx_52 ON Submission
(
 cid
);
