
import datetime
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import time


mysql_host = "localhost"
def connect():
	con = mysql.connector.connect(
		host=mysql_host,
		user="dbexamuser",
		database="examdb",
		passwd="dbExam.group7",
		use_pure=True,
	)
	con.autocommit = False
	mycursor = con.cursor(cursor_class=MySQLCursorPrepared)
	return con, mycursor

while True:
	con, mycursor = connect()
	
	
	sql = "select count(*) from books;"
	
	now = datetime.datetime.now()

	mycursor.execute(sql)
	count = mycursor.fetchone()[0]
	
	millis_run = (datetime.datetime.now() - now).total_seconds() * 1000
	
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print("Book count: {}".format(count))
	print("Milliseconds: {}".format(millis_run))
	
	mycursor.close()
	con.close()
	time.sleep(10)

