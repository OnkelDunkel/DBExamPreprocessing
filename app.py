import sys
import datetime
import folium
import mysql.connector

#arr = [1,2,3,4]

#print(arr[3:][0])

def do_mysql(sql, insert_values):
	now = datetime.datetime.now()
	con = mysql.connector.connect(
		host="139.59.140.52",
		user="dbexamuser",
		database="examdb",
		passwd="dbExam.group7",
		use_pure=True,
	)
	con.autocommit = False
	mycursor = con.cursor(prepared=True)
	mycursor.execute(sql, insert_values)
	result = mycursor.fetchall();
	mycursor.close()
	con.close()
	millis = (datetime.datetime.now() - now).total_seconds() * 1000
	return result, millis
	
def mysql_q1(param):
	insert_values = (param[0],)
	sql = """
	select title from books join (
		select authors.id "author_id"
		from books, authors, books_cities, cities
		where cities.name = %s
		and cities.id = books_cities.cityid
		and books_cities.bookid = books.id
		and books.authorid = authors.id
	) as books_w_city
	on books.id = books_w_city.author_id;
	"""
	result, millis = do_mysql(sql, insert_values)
	for r in result:
		print("- '{}'".format(r[0]))
	return millis

def mysql_q2(param):
	insert_values = (param[0],)
	sql = """
	select cities.name, latitude, longtitude
	from cities, books_cities, books
	where books.title = %s
	and cities.id = books_cities.cityid
	and books_cities.bookid = books.id;
	"""
	result, millis = do_mysql(sql, insert_values)
	if len(result) > 0:
		m = folium.Map(
			location=[result[0][1], result[0][2]],
			zoom_start=1,
			tiles='Stamen Terrain'
		)
		for r in result:
			folium.Marker(
				location=[r[1], r[2]],
				popup=r[0],
				icon=folium.Icon(color='red')
			).add_to(m)
			
			print("- '{}'".format(r[0]))
		html_name = "q2.html"
		m.save(html_name)
		print("See map in '{}'".format(html_name))
	else:
		print("no results, no map")
	return millis
	
def mysql_q3(param):
	insert_values = (param[0],)
	sql = """
	select title, cities.name, latitude, longtitude
	from books, authors, cities, books_cities
	where authors.name = %s
	and books.authorid = authors.id
	and books_cities.bookid = books.id
	and books_cities.cityid = cities.id;
	"""
	result, millis = do_mysql(sql, insert_values)
	if len(result) > 0:
		books = []
		m = folium.Map(
			location=[result[0][2], result[0][3]],
			zoom_start=1,
			tiles='Stamen Terrain'
		)
		for r in result:
			books.append(r[0])
			folium.Marker(
				location=[r[2], r[3]],
				popup=r[1],
				icon=folium.Icon(color='red')
			).add_to(m)
			
			print("- '{}'".format(r[0]))
		html_name = "q3.html"
		m.save(html_name)
		print("See map in '{}'".format(html_name))
		print("Books by author")
	else:
		print("no results, no map")
	return millis
	
def mysql_q4(param):
	insert_values = (param[0],param[1])
	sql = """
	select title, city_w_distance.dist from books join (
		select 
		st_distance_sphere(
			cities.location, 
			point( %s , %s )
		) as "dist",
		books_cities.bookid "book_id"
		from books_cities, cities
		where cities.id = books_cities.cityid
	) as city_w_distance
	on books.id = city_w_distance.book_id
	where city_w_distance.dist < 10000
	limit 10;
	"""
	print("Query not working:")
	print(sql % insert_values)
	return

	print(sql % insert_values)
	result, millis = do_mysql(sql, insert_values)
	print(result)
	#for r in result:
		#print("- '{}'".format(r[0]))
	return millis

	
def mongodb_q1(param):
	print("q1")
	
def mongodb_q2(param):
	print("q2")
	
def mongodb_q3(param):
	print("q3")
	
def mongodb_q4(param):
	print("q4")


def run_q(db_type, query_name, param):
	dbs = {
		"mysql" : {
			"q1" : mysql_q1,
			"q2" : mysql_q2,
			"q3" : mysql_q3,
			"q4" : mysql_q4,
		},
		"mongodb" : {
			"q1" : mongodb_q1,
			"q2" : mongodb_q2,
			"q3" : mongodb_q3,
			"q4" : mongodb_q4,
		},
	}
	try:
		now = datetime.datetime.now()
		db_millis = dbs[db_type][query_name](param)
		func_millis = (datetime.datetime.now() - now).total_seconds() * 1000
		print("Function ran for {0:.4f} milliseconds".format(func_millis))
		print("The DB query took {0:.4f} milliseconds".format(db_millis))
		return func_millis, db_millis
	except KeyError:
		print("unknown db type or query")
	except TypeError:
		print("function did not finish")

def run_app(db_type, query_name, param):
	db_type = db_type.lower()
	query_name = query_name.lower()
	#print("run query '{}' with '{}'".format(db_type, query_name))
	
	run_q(db_type, query_name, param)


if len(sys.argv) == 4 or len(sys.argv) == 5:
	#print(sys.argv)
	run_app(sys.argv[1], sys.argv[2], sys.argv[3:])
elif len(sys.argv) == 3 and sys.argv[2] == "test":
	db_type = sys.argv[1]
	times=[]
	
	times.append(run_q(db_type, "q1", ["London"]))
	times.append(run_q(db_type, "q1", ["Berlin"]))
	times.append(run_q(db_type, "q1", ["Tokyo"]))
	times.append(run_q(db_type, "q1", ["Washington"]))
	times.append(run_q(db_type, "q1", ["Copenhagen"]))
	
	
	times.append(run_q(db_type, "q2", ["The Greatest Thing In the World and Other Addresses"]))
	times.append(run_q(db_type, "q2", ["Toronto of Old"]))
	times.append(run_q(db_type, "q2", ["Margery, Volume 5."]))
	times.append(run_q(db_type, "q2", ["The Four Corners of the World"]))
	times.append(run_q(db_type, "q2", ["Blackwood's Edinburgh Magazine, Vol. 68, No 422, December 1850"]))
	
	times.append(run_q(db_type, "q3", ["Laura F. Kready"]))
	times.append(run_q(db_type, "q3", ["Maria Louise Pool"]))
	times.append(run_q(db_type, "q3", ["B. Perez Galdos"]))
	times.append(run_q(db_type, "q3", ["C. F. Wimberly"]))
	times.append(run_q(db_type, "q3", ["Robert Folkestone Williams"]))
	
	#times.append(run_q(db_type, "q4", [20, 70]))
	#times.append(run_q(db_type, "q4", [70, 170]))
	#times.append(run_q(db_type, "q4", [-20, 10]))
	#times.append(run_q(db_type, "q4", [-10, -170]))
	#times.append(run_q(db_type, "q4", [1, 7]))
	
	func_total = 0
	db_total = 0
	for t in times:
		func_total += t[0]
		db_total += t[1]
	print("Total time for functions: {}".format(func_total))
	print("Total time for db queries: {}".format(db_total))
	
elif len(sys.argv) == 2 and sys.argv[1] == "help":
	print("""
The application takes in following arguments:
[DB type]
[query name]
[query parameter (city name|book title|author name|latitude)]
[query parameter (longtitude)]

The available DBs are:
[mysql, mongodb]

The available queries are corresponding to the assignment description:
[q1, q2, q3, q4]

Example query:
python app.py mysql q4
	""")
else:
	print("insufficient arguments")

print("end")
