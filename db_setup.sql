
CREATE USER IF NOT EXISTS 
	'dbexamuser'@localhost IDENTIFIED BY 'dbExam.group7';
	
DROP DATABASE IF EXISTS examdb;
CREATE DATABASE examdb;

GRANT DELETE, INSERT, SELECT, UPDATE ON examdb.* TO dbexamuser@localhost;
FLUSH PRIVILEGES;

USE examdb;

CREATE TABLE authors (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name NVARCHAR(100)
);
CREATE TABLE books (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title NVARCHAR(1000),
	authorid INT NOT NULL,
	FOREIGN KEY (authorid) REFERENCES authors(id)
);
CREATE TABLE cities (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name NVARCHAR(200),
	location POINT
);
CREATE TABLE books_cities (
	bookid INT NOT NULL,
	cityid INT NOT NULL,
	FOREIGN KEY (bookid) REFERENCES books(id),
	FOREIGN KEY (cityid) REFERENCES cities(id),
	CONSTRAINT uc_books_cities UNIQUE (bookid,cityid)
);





