from os import listdir
import en_core_web_sm
import datetime
import re
import json


#******************************* missing do sql

def get_city_names(text):
	global nlp
	doc = nlp(text)
	locs = []
	for ent in doc.ents:
		if ent.label_ == "GPE":
			locs.append(ent.text)
			
	return locs

def create_chunks(file_text, size):
	global max_file_length
	return [file_text[i:i+size] for i in range(0, len(file_text), size)]

def extract_details(file_text):
	re_patterns = [
		"[ ]{0,4}Title: (.+)\n\n[ ]{0,4}Author: ([^\n]+)\n",
		"  We need your donations.\n\n\n([^\n]+)\n\nby ([^\n]+)\n\n",
		"\n\nTitle: (.+)\nAuthor: (.+)\nRelease Date: ",
		"\n\n\n\n\n\n[\d]{4}\n\n()\n\nby ()\n\n\nDramatis Personae",
	]
	title = None
	author = None

	for pattern in re_patterns:
		try:
			result = re.search(pattern, file_text, re.DOTALL)
			title = result.group(1)
			author = result.group(2)
			break
		except:
			continue
	
	return title, author


nlp = en_core_web_sm.load()
books = []
max_file_length = 100000 * 2
txt_files = [f for f in listdir() if f.endswith(".txt")]

now = datetime.datetime.now()
large_files = 0
total_errors = 0
encoding_errors = 0
format_errors = 0
counter = 0

def status():
	global large_files, total_errors, format_errors, encoding_errors, now
	
	secs_run = (datetime.datetime.now() - now).total_seconds()
	
	print("big_files: {}".format(large_files))
	print("total_errors: {}".format(total_errors))
	print("format_errors: {}".format(format_errors))
	print("encoding_errors: {}".format(encoding_errors))
	print("seconds: {}".format(secs_run))
	minutes = secs_run/60
	print("minutes: {}".format(minutes))
	print("estimate: {} minutes left".format(((len(txt_files)-counter)/counter)*minutes))
	print("file {} / {}".format(counter, len(txt_files)))

for file_name in txt_files:
	#file_name = "617.txt"
	counter += 1
	
	with open(file_name, 'r') as file:
		print("***************************************")
		print(file_name)
		status()

		try:
			file_text = file.read()
			
			title, author = extract_details(file_text)
			
			if author == None or title == None:
				format_errors += 1
				total_errors += 1
				print(file_name + "********ERROR FINDING DETAILS*****************")
				continue
			
			#print("title: {}".format(title))
			#print("author: {}".format(author))
			
			parts = create_chunks(file_text, max_file_length)
			char_count = len(file_text)
			
			if(char_count >= max_file_length):
				print("No of chars: {}".format(char_count))
				print("---------------BIG FILE---------------")
				large_files += 1
			
			city_names = []
			
			for t in parts:
				city_names.extend(get_city_names(t))
			
			city_names = list(set(city_names))
			
			book = {
				"title":title, 
				"author":author,
				"city_names":city_names,
			}
			
			books.append(book)
			
			print(json.dumps(book))
			
		except UnicodeDecodeError:
			total_errors += 1
			encoding_errors += 1
			print(file_name + "********ENCODING ERROR*****************")
	#break
			

status()

#print(json.dumps(books))

with open("books_processed.json", 'w') as fout: 
	fout.write(json.dumps(books))
