DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tg_user;
DROP TABLE IF EXISTS tg_permits;
DROP TABLE IF EXISTS tg_user_permits;

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
    tg_id    INTEGER UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE tg_permits
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT NOT NULL
);

CREATE TABLE tg_user_permits
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_user   INTEGER NOT NULL,
    tg_permit INTEGER NOT NULL
);

INSERT INTO tg_permits (title)
VALUES
  ('post links'),
  ('post media')
