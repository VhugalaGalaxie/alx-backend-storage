-- Creates a table users with below attributes
-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)
-- country, enum of countries: US, CO and TN, never null (default=US)
-- If table exists, script will not fail, can be executed on any database

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
       id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
       email VARCHAR(255) NOT NULL UNIQUE,
       name VARCHAR(255),
       country CHAR(2) NOT NULL DEFAULT 'US' CHECK (country IN ('US', 'CO', 'TN'))
);
