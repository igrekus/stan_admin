DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tg_user;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL,
    tg_user  INTEGER,
    FOREIGN KEY(tg_user) REFERENCES tg_user(id)
);

CREATE TABLE tg_user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT UNIQUE NOT NULL,
    last_name TEXT UNIQUE NOT NULL
);
