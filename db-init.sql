DROP DATABASE IF EXISTS demodb1;

CREATE DATABASE IF NOT EXISTS demodb1;

USE demodb1;

CREATE TABLE IF NOT EXISTS company (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(32) NOT NULL,
    company_domain VARCHAR(32),
    created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_on DATETIME
);

CREATE TABLE IF NOT EXISTS user (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    company_id INT,
    created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_on DATETIME,
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

INSERT INTO company (company_id, company_name, company_domain) VALUES 
(1, 'Company One Ltd', 'companyone.com'),
(2, 'Hats Eleven', 'hats11.com'),
(3, 'Roses', 'roses.com'),
(4, 'Chocolates Steamer', 'chocolates.com');

INSERT INTO user (user_id, first_name, last_name, company_id) VALUES
(1, 'Alejandro', 'G', 1),
(2, 'Michael', 'N', 1),
(3, 'Frankie', 'W', 2),
(4, 'Patty', 'P', 4),
(5, 'Harvey', 'E', 3),
(6, 'Frank', 'S', 3);

/*
SELECT * FROM company c JOIN user u ON c.company_id = u.company_id;

-- test deleting user
SELECT SLEEP(5);

SET @deleted_user_id = 3;

UPDATE user SET deleted_on = now() WHERE user_id = @deleted_user_id;

SELECT user_id, first_name, last_name,
    unix_timestamp(created_on) AS 'created_on_unix_ts',
    unix_timestamp(updated_on) AS 'updated_on_unix_ts',
    unix_timestamp(deleted_on) AS 'deleted_on_unix_ts'
FROM user WHERE user_id = @deleted_user_id;
*/