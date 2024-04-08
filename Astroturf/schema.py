

CREATE TABLE users(
    userid INTEGER PRIMARY KEY, 
    username TEXT, 
    account_creation_date TEXT, 
    account_deletion_date TEXT)

CREATE TABLE posts (
	postid INTEGER PRIMARY KEY, 
	title TEXT,
	url TEXT,
	comments_url TEXT, 
	upvotes INTEGER,
	date_created TEXT, 
	date_deleted TEXT,
    reddit_post_id TEXT,
	userid INTEGER,
	FOREIGN KEY(userid) REFERENCES users(userid)
	);

CREATE TABLE comments (
    commentid INTEGER PRIMARY KEY,
    content TEXT,
    date_created TEXT,
    date_deleted TEXT,
    userid INTEGER,
    postid INTEGER,
    FOREIGN KEY(userid) REFERENCES users(userid),
    FOREIGN KEY(postid) REFERENCES posts(postid)
    );