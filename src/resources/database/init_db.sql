-- Table Account
CREATE TABLE Account
(
    twitter_handle TEXT NOT NULL,
    followed_timestamp TIME NOT NULL,
    CONSTRAINT PK_ACCOUNT PRIMARY KEY (twitter_handle)
);
