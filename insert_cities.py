import pandas as pd
import datetime
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared


df = pd.read_csv("worldcitiespop.csv")

def clean_cities():
	global df
	print("City count before clean: {}".format(df.count()[0]))
	
	df = df[df["AccentCity"].notna()]
	df = df[df["Latitude"].notna()]
	df = df[df["Longitude"].notna()]
	
	df = df.sort_values(["Population"], ascending=False)
	df = df.drop_duplicates(subset=["AccentCity"], keep="first")
	
	print("City count after clean: {}".format(df.count()[0]))

	
def open_con():
	con = mysql.connector.connect(
		host="localhost",
		user="dbexamuser",
		database="examdb",
		passwd="dbExam.group7",
		use_pure=True,
	)
	con.autocommit = False
	mycursor = con.cursor(cursor_class=MySQLCursorPrepared)
	return con, mycursor

def insert_cities():
	global con, mycursor
	now = datetime.datetime.now()
	counter = 1
	interval_counter = 0
	commit_interval = 1000
	
	sql = "INSERT INTO examdb.cities (name, location) VALUES (%s, Point(%s , %s));"
	
	for i, row in df.iterrows():
		city_name = row["AccentCity"]
		city_long = row["Longitude"]
		city_lat = row["Latitude"]
		
		insert_values = (city_name, city_lat, city_long)
		
		mycursor.execute(sql, insert_values)
		
		if (counter >= interval_counter + commit_interval):
			print(mycursor.statement)
			print(sql % insert_values)
			con.commit()
			interval_counter += commit_interval
			print(counter)
			
		counter += 1
		
	con.commit()
	
	time_diff = datetime.datetime.now() - now
	print("***************************************************")
	print("Time in seconds: {}".format(time_diff.total_seconds()))
	print("***************************************************")

def close_con():
	global con, mycursor
	mycursor.close()
	con.close()


	
clean_cities()
con, mycursor = open_con()
insert_cities()
close_con()





