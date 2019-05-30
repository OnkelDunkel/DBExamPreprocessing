import pymongo
import json
import mysql.connector


con = mysql.connector.connect(
	host="139.59.140.52",
	user="dbexamuser",
	database="examdb",
	passwd="dbExam.group7",
	use_pure=True,
)
con.autocommit = False
mycursor = con.cursor()
mycursor.execute("select * from books join authors on books.authorid = authors.id;")
result = mycursor.fetchall();
print(len(result))
print(result[0])
books = result
mycursor.close()
con.close()


con = mysql.connector.connect(
	host="139.59.140.52",
	user="dbexamuser",
	database="examdb",
	passwd="dbExam.group7",
	use_pure=True,
)
con.autocommit = False
mycursor = con.cursor()
mycursor.execute("select * from books_cities;")
result = mycursor.fetchall();
print("books_cities")
print(len(result))
print(result[0])
bookscities = result
mycursor.close()
con.close()

booksdict = {}

for b in books:
	bookid = b[0]
	book = {
		"_id" : bookid,
		"title" : b[1],
		"author" : b[4],
		"cities" : [],
	}
	booksdict[bookid]=book

for bc in bookscities:
	bookid = bc[0]
	booksdict[bookid]["cities"].append(bc[1])

with open ("books.json", "w") as fout:
	json.dump(list(booksdict.values()), fout)
	
print(booksdict[8409])
	
#bc[1] for bc in bookscities if bc[0] == bookid	


con = mysql.connector.connect(
	host="139.59.140.52",
	user="dbexamuser",
	database="examdb",
	passwd="dbExam.group7",
	use_pure=True,
)
con.autocommit = False
mycursor = con.cursor()
mycursor.execute("select * from cities;")
result = mycursor.fetchall();
print(len(result))
print(result[0])
cities = result
mycursor.close()
con.close()


citieslist = []

for c in cities:
	id = c[0]
	city = {
		"_id" : id,
		"name" : b[1],
		"latitude" : b[2],
		"longtitude" : b[3],
	}
	citieslist.append(city)

with open ("cities.json", "w") as fout:
	json.dump(citieslist, fout)
