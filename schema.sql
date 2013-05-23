DROP TABLE IF EXISTS reply;
DROP TABLE IF EXISTS upimage;

CREATE TABLE upimage (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    title TEXT,
    message TEXT,
    img TEXT NOT NULL,
    thumb TEXT NOT NULL,
    delkey TEXT,
    deltime DATETIME,
    last_modified DATETIME,
    reply_count INTEGER
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE reply (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    parent_id INTEGER NOT NULL,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    title TEXT,
    message TEXT,
    img TEXT,
    thumb TEXT,
    delkey TEXT,
    deltime DATETIME,
    foreign key (`parent_id`)
        references `upimage` (`id`)
        on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

