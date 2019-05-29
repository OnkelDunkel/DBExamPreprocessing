/* query 1 */
select title from books join (
	select authors.id "author_id"
	from books, authors, books_cities, cities
	where cities.name = "Paris"
	and cities.id = books_cities.cityid
	and books_cities.bookid = books.id
	and books.authorid = authors.id
) as books_w_city
on books.id = books_w_city.author_id;



/* query 2 */
select latitude, longtitude
from cities, books_cities, books
where books.title = '1995 United States Congressional Address Book'
and cities.id = books_cities.cityid
and books_cities.bookid = books.id;



/* query 3 */











