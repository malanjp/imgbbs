DROP TABLE IF EXISTS upimage;
CREATE TABLE upimage (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    title TEXT,
    message TEXT,
    img TEXT NOT NULL,
    thumb TEXT NOT NULL,
    delkey TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS reply;
CREATE TABLE reply (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    parent_id INTEGER NOT NULL,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    title TEXT,
    message TEXT,
    img TEXT NOT NULL,
    thumb TEXT NOT NULL,
    delkey TEXT,
    foreign key (`parent_id`)
        references `upimage` (`id`)
        on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

