-- Create Tables Script
-- Label
CREATE TABLE IF NOT EXISTS label
(
 lid  uuid NOT NULL,
 name text NOT NULL,
 CONSTRAINT PK_label PRIMARY KEY ( lid )
);

-- photo
CREATE TABLE IF NOT EXISTS Photo
(
 pid  uuid NOT NULL,
 "path" text NOT NULL,
 CONSTRAINT PK_photo PRIMARY KEY ( pid )
);

-- user
CREATE TABLE IF NOT EXISTS "User"
(
 uuid           uuid NOT NULL,
 username       text NOT NULL,
 password       text NOT NULL,
 trust          float NOT NULL,
 ProfilePicture text NOT NULL,
 CONSTRAINT PK_user PRIMARY KEY ( uuid )
);

-- classification
CREATE TABLE IF NOT EXISTS Classification
(
 cuid            uuid NOT NULL,
 photoId         uuid NOT NULL,
 label           uuid NOT NULL,
 confidence      float GENERATED ALWAYS AS (trueCount / (trueCount+falseCount)) STORED,
 trueCount       int NOT NULL,
 falseCount      int NOT NULL,
 isSourceOfTruth boolean NOT NULL,
 pid             uuid NOT NULL,
 lid             uuid NOT NULL,
 CONSTRAINT PK_classification PRIMARY KEY ( cuid ),
 CONSTRAINT FK_39 FOREIGN KEY ( pid ) REFERENCES Photo ( pid ),
 CONSTRAINT FK_45 FOREIGN KEY ( lid ) REFERENCES label ( lid )
);

-- userclassification
CREATE TABLE IF NOT EXISTS UserClassification
(
 ucuid        uuid NOT NULL,
 correctLabel boolean NOT NULL,
 uuid         uuid NOT NULL,
 cuid         uuid NOT NULL,
 CONSTRAINT PK_userclassification PRIMARY KEY ( ucuid ),
 CONSTRAINT FK_48 FOREIGN KEY ( uuid ) REFERENCES "User" ( uuid ),
 CONSTRAINT FK_51 FOREIGN KEY ( cuid ) REFERENCES Classification ( cuid )
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

CREATE INDEX fkIdx_49 ON UserClassification
(
 uuid
);

CREATE INDEX fkIdx_52 ON UserClassification
(
 cuid
);