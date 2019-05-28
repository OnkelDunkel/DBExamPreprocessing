
CREATE USER IF NOT EXISTS 
	'dbexamuser'@'localhost' IDENTIFIED BY 'dbExam.group7';
CREATE USER IF NOT EXISTS 
	'dbexamuser'@'%' IDENTIFIED BY 'dbExam.group7';
	
DROP DATABASE IF EXISTS examdb;
CREATE DATABASE examdb;

GRANT DELETE, INSERT, SELECT, UPDATE ON examdb.* TO dbexamuser@localhost;
GRANT DELETE, INSERT, SELECT, UPDATE ON examdb.* TO dbexamuser@%;
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

drop procedure if exists insert_book;
delimiter $$
create procedure insert_book(in booktitle nvarchar(1000), in authorname nvarchar(100))
begin
	DECLARE author_id INT default 0;
	DECLARE book_id iNT default 0;
	set @author_id = 0;
	set @book_id = 0;

	select id into @author_id from authors where name = authorname limit 1;

	if @author_id is null or @author_id = 0 then
		insert into authors(name) values (authorname);
		set @author_id = LAST_INSERT_ID();
	end if;

	select id into @book_id from books 
		where authorid = @author_id 
		and title = booktitle
		limit 1;

	if @book_id is null or @book_id = 0 then
		insert into books(title, authorid) values (booktitle, @author_id);
		set @book_id = LAST_INSERT_ID();
	end if;
	select @book_id;
end$$
delimiter ;

																					 
drop procedure if exists create_city_book_relation;
delimiter $$
create procedure create_city_book_relation(in book_id int, in city_name nvarchar(200))
begin
	DECLARE city_id iNT default 0;
	set @city_id = 0;

	select id into @city_id from cities where name = city_name limit 1;

	if @city_id is not null and not @city_id = 0 then
		insert into books_cities(bookid, cityid) values (book_id, @city_id);
	end if;

	select @city_id;
end$$
delimiter ;





