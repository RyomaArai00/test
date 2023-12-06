DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS company;

-- user テーブル
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

-- post テーブル
CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES user (id)
);

-- comment テーブル
CREATE TABLE comment (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	post_id INTEGER NOT NULL,
	comment TEXT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES user (id),
	FOREIGN KEY (post_id) REFERENCES post (id)
);

-- company テーブル
CREATE TABLE company (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	cnt INTEGER NOT NULL,
	keyword TEXT NOT NULL,
	rank INTEGER NOT NULL,
	title TEXT NOT NULL,
	url TEXT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES user (id)
);
