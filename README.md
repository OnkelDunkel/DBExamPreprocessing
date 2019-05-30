# Database Exam Project

### Group name: The Light

### Group members: Ali Raza Khan, Mohammed Murad Hossain Sarker, Rasmus Balder Nordbjærg, Yakubu Adeyemi Oseni

## Databases are used

We used MySQL and mongodb. We use mongodb because it is high     performance and simple to install. It has the freedom of using JSON or BSON document to store data.
We use mysql because it is relational database and wide range used including data warehousing, e-commerce. Also, it is free and open source.

## How data is modeled in the database?

The data is set up on a DigitalOcean VM:

We have insert cityname  and location in the citis table and  insert booktitle and authorid in the books table then create relation between books and authors table. We have also create new table name books_cities for create many to many relationship between books and cities table.

Due to the lightweightness of our application we are not exactly modelling the data in the application. That is we do not have dedicated classes to store the models in.

![DB diagram](images/db_diagram.png)

## Importing the data

### Getting the .txt book files from the Gutenberg Project

We followed the hinted steps creating a VM on DigitalOcean using Vagrant. In the vagrantfile we changed the size of the VM from '1gb' to 's-1vcpu-3gb' because we believed this would better fit our needs.

After for running less than 2 days the script was done and we could download the 5gb archive.tar using scp. Extracting the archive.tar file revealed directory with around 37,000 zipfiles.

### Unzipping the files and putting them into order

We ran below shell commands from the directory of all the zipped files in order to unzip them and thereafter delete the zip files:

    unzip '*.zip'
    rm *.zip

Following commands was used to move files from subfolders to current folder, delete empty folders and show all non-txt files:

	find . -mindepth 2 -type f -print -exec mv {} . \;
	find . -empty -type d -delete
	find -not -iname "*.txt"

Last line gave following ouput. Only few files that aren't .txt:

	./13655.txt.20041109
	./Common-README
	./25438-h.htm
	./001.png
	./17424-mid.mid
	./17424-mus.mus
	./17424-pdf.pdf
	./17421-mid.mid
	./17421-mus.mus
	./17421-pdf.pdf
	./17423-mid.mid
	./17423-mus.mus
	./17423-pdf.pdf
	./17422-mid.mid
	./17422-mus.mus
	./17422-pdf.pdf
	./anxious.jpg
	./christmas.jpg
	./detail.jpg
	./fairy.jpg
	./horse.jpg
	./last.jpg
	./spring.jpg
	./summer.jpg

We deleted all the non-txt files:

	find -not -iname "*.txt" -delete


### Getting author and book title from txt

(see books_processing/process_books.py)

We used below regular expression patterns to extract the author and the book title from the txt files. 

	re_patterns = [
        "[ ]{0,4}Title: (.+)\n\n[ ]{0,4}Author: ([^\n]+)\n",
        "  We need your donations.\n\n\n([^\n]+)\n\nby ([^\n]+)\n\n",
        "\n\nTitle: (.+)\nAuthor: (.+)\nRelease Date: ",
        "\n\n\n\n\n\n[\d]{4}\n\n()\n\nby ()\n\n\nDramatis Personae",
    ]

By testing with a sample of 1000 txt files we concluded that around 5% of the files would be last with our algorithm. This was due to either text encoding not being utf-8 or our regex was not able to extract the book title and author. We agreed that this was an acceptable loss.

### Using the NLP python library spaCy we extracted all named entities from the books

(see books_processing/process_books.py)

Using the name entity recognition provided by the spaCy library the entities are divided into types (categories) so we only included entities of type 'GPE' which should include countries, cities and states.

The spaCy library was rather heavy and had a default maximum length of 1,000,000 characters per string. Following the library recommendation we set the max limit to be even lower (ram available * 10,000). Some books exceeded the max length so we cut them into chunks accordingly.

We divided the data into 8 parts and set up 6 DigitalOcean VM and to of our own machines to process the data. We managed to proces and upload around 15.000 books. When everything was running smoothly we reached a speed of processing and uploading around 1500 books per hour.

### Uploading the books and their city mentions

(see sql/db_setup.sql & load_cities_to_db.ipynb)

In the MySQL database we had created a stored procedure to insert a book. Since the books table contains a foreign key column referencing the authors we need to have an author id before the book can be inserted. Therefore we check whether the author exists and if not we insert into the authors table.
When creating the insert_book stored procedure we decided that if 2 books with same title have different authors they must be different books. Should we try to insert a book with same author and title as an existing book our system will recognise it as the same book and therefore not perform the insert statement.

	drop procedure if exists insert_book;
	delimiter $$
	create procedure insert_book(
		in booktitle nvarchar(1000), 
		in authorname nvarchar(100)
	)
	begin
		DECLARE author_id INT default 0;
		DECLARE book_id iNT default 0;
		set @author_id = 0;
		set @book_id = 0;

		select id into @author_id from authors 
			where name = authorname limit 1;

		if @author_id is null or @author_id = 0 then
			insert into authors(name) values (authorname);
			set @author_id = LAST_INSERT_ID();
		end if;

		select id into @book_id from books 
			where authorid = @author_id 
			and title = booktitle
			limit 1;

		if @book_id is null or @book_id = 0 then
			insert into books(title, authorid) 
				values (booktitle, @author_id);
			set @book_id = LAST_INSERT_ID();
		end if;
		select @book_id;
	end$$
	delimiter ;

We called a different stored procedure to update the many to many relation between the books and the cities:

	drop procedure if exists create_city_book_relation;
	delimiter $$
	create procedure create_city_book_relation(in city_name nvarchar(200), in book_id int)
	begin
		DECLARE city_id iNT default 0;
		set @city_id = 0;

		select id into @city_id from cities where name = city_name limit 1;

		if @city_id is not null and @city_id > 0 then
			insert into books_cities(bookid, cityid) values (book_id, @city_id);
		end if;

		select @city_id;
	end$$
	delimiter ;

If a city with the given name does not exists in our database we don insert a book to city relation. The reason for this is because we dont want to store cities in the DB that we dont know the lat and long of. Another reason is that the NLP linbrary we used doesnt distingusih between cities, states and countries.

## The application

(See app.py)

In order to run the application you will need to install folium and mysql connector libraries.

	pip install folium
	pip install mysql-connector-python

Our application is a python command line application. The application can be run with following commands wihtout parenthesis:

* python app.py (mysql|mongodb) (test|q1|q2|q3|q4) (param1) (param1 only for q4 then longitude)

Running the tests with the mysql database we can see that around 90% of the time was used on the db queries for all the test queries. However this number was even higher for query 1 that was not dealing with maps.

## Recommendation for choice of DB

We will recommend MySQl for this dataset. This is mainly due to the fact that we do not imagine a lot of changes happening to the structure of the data. With MySQL we also have great support for the ACID with foreign keys and transactions.
The strength of MongoDB is that it is very flexible when it comes to the structure of the data. That can be a benefit in the right situations but in this business we dont imagine changing data structure to be an issue.
