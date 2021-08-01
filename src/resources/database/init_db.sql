-- Table Account
CREATE TABLE Account
(
    twitter_handle TEXT NOT NULL,
    followed_timestamp TIME NOT NULL,
    CONSTRAINT PK_ACCOUNT PRIMARY KEY (twitter_handle)
);

-- Table Tweet
CREATE TABLE Tweet
(
    tweet_id INTEGER NOT NULL
    tweet_group_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    twitter_handle TEXT NOT NULL,
    published_date TIME NOT NULL,
    tweet_text TEXT NOT NULL,
    CONSTRAINT PK_TWEET PRIMARY KEY(tweet_id),
    CONSTRAINT FK_TWEET_TWEET_GROUP FOREIGN KEY (tweet_group_id) REFERENCES TweetGroup (group_id)
);

-- Table TweetGroup
CREATE TABLE TweetGroup
(
    group_id INTEGER NOT NULL,
    group_created TIME NOT NULL,
    CONSTRAINT PK_TWEET_GROUP PRIMARY KEY(group_id)
);