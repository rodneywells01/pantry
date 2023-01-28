DROP DATABASE IF EXISTS pantry;
CREATE DATABASE pantry;
\c pantry;


DROP TABLE IF EXISTS inventory;


CREATE TABLE inventory(
	ID SERIAL PRIMARY KEY     NOT NULL,
	USER_ID VARCHAR(50) NOT NULL,
	UPC VARCHAR(13) NOT NULL,
	QTY_PERCENTAGE_REMAINING NUMERIC NOT NULL
);

DROP TABLE IF EXISTS product_info;
CREATE TABLE product_info(
	ID SERIAL PRIMARY KEY     NOT NULL,
	TITLE TEXT NOT NULL,
	DESCRIPTION TEXT,
	EAN VARCHAR(13) NOT NULL,
	UPC VARCHAR(13) NOT NULL,
	BRAND TEXT NOT NULL,
	MODEL TEXT,
	CATEGORY TEXT NOT NULL,
	IMAGE_URL TEXT
);



-- DROP TABLE IF EXISTS product_info;
-- CREATE TABLE product_info(
-- 	ID SERIAL PRIMARY KEY     NOT NULL,
-- 	TITLE TEXT NOT NULL,
-- 	DESCRIPTION TEXT,
-- 	EAN VARCHAR(13) NOT NULL,
-- 	UPC VARCHAR(13) NOT NULL,
-- 	BRAND TEXT NOT NULL,
-- 	MODEL TEXT,
-- 	CATEGORY TEXT NOT NULL,
-- 	IMAGE_URL TEXT
-- );


-- Create extension for UUID Generation. Postgres does not support
-- this by default.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	ID SERIAL PRIMARY KEY     NOT NULL,
	USER_ID uuid DEFAULT uuid_generate_v4(),
	EMAIL VARCHAR(50) UNIQUE,
	FIRST_NAME VARCHAR(50) NOT NULL,
	LAST_NAME VARCHAR(50) NOT NULL
);

-- Sample User
INSERT INTO users(email, first_name, last_name) VALUES (
	'rodneywells01@gmail.com',
	'Rodney',
	'Wells'
);


-- Sample Inventory
-- INSERT INTO inventory(user_id, item_name, qty_percentage_remaining)
-- VALUES (
-- 	'123',
-- 	'Toilet Paper',
-- 	1.0
-- );


-- INSERT INTO inventory(user_id, item_name, qty_percentage_remaining)
-- VALUES (
-- 	'1238092183',
-- 	'Tissues',
-- 	0.5
-- );

-- INSERT INTO domain (name, category, photo_url, description)
-- VALUES
-- (
-- 	'facebook',
-- 	'Cancer',
-- 	'https://www.facebook.com/images/fb_icon_325x325.png',
-- 	'This shit sucks your soul dry.'
-- );

commit;