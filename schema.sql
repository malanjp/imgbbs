CREATE TABLE upimage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    title TEXT,
    message TEXT,
    img TEXT NOT NULL,
    thumb TEXT NOT NULL,
    delkey TEXT
);
