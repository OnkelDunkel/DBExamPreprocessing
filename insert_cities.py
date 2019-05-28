import pandas as pd
import datetime
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared


df = pd.read_csv("worldcitiespop.csv")

def clean_cities():
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
	return con, cursor

def insert_cities():
    now = datetime.datetime.now()
    large_sql = ""
    counter = 1
    interval_counter = 0
    interval = 1000
	
	
	sql = """INSERT INTO examdb.cities (name, location) 
		VALUES (%s, Point(%s , %s));"""
    
    for i, row in df.iterrows():
        city_name = row["AccentCity"]
        city_long = row["Longitude"]
        city_lat = row["Latitude"]
        #sql = "INSERT INTO authors (name) VALUES ('bob');"
        #large_sql += sql
        
        insert_values = (city_name, city_lat, city_long)
        
        #print(sql % insert_values)
        #print("city name: ")
        #print(type(city_name))
        #print(counter)
        
        mycursor.execute(sql, insert_values)
        #print(mycursor.statement)
        
        if (counter >= interval_counter + interval):
            print(mycursor.statement)
            con.commit()
            interval_counter += interval
            print(counter)
            
        counter += 1
        
    #print(large_sql)
    #mycursor.execute(large_sql, multi = True)
    con.commit()
    
    time_diff = datetime.datetime.now() - now
    print(time_diff.total_seconds())

	
	
con.close()
mycursor.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	