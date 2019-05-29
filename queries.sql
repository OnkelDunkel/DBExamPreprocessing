/* query 1 */
select title from books join (
	select authors.id "author_id"
	from books, authors, books_cities, cities
	where cities.name = 'Paris'
	and cities.id = books_cities.cityid
	and books_cities.bookid = books.id
	and books.authorid = authors.id
) as books_w_city
on books.id = books_w_city.author_id;

select authors.name from authors, books where books.authorid = authors.id and books.id = 2383;

/* query 2 */
select cities.name, latitude, longtitude
from cities, books_cities, books
where books.title = '1995 United States Congressional Address Book'
and cities.id = books_cities.cityid
and books_cities.bookid = books.id;



/* query 3 */
select title, cities.name, latitude, longtitude
from books, authors, cities, books_cities
where authors.name = 'Robert Louis Stevenson'
and books.authorid = authors.id
and books_cities.bookid = books.id
and books_cities.cityid = cities.id;



/* query 4 */
select title
from books, cities_books, cities
where st_distance_sphere(
	cities.location, point( 55.6761 , 12.5683 )
) <= 10000
and books_cities.cityid = cities.id
and books_cities.bookid = books.id;



