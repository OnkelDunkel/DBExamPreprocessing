from os import listdir
from os import rename
import os

txt_files = [f for f in listdir() if f.endswith(".txt")]

folder_count = 8
counter = 0

for txt in txt_files:
	counter += 1
	dir_name = str(counter)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
	rename(txt, dir_name + "/" + txt)
	#print(counter)
	if counter >= folder_count:
		counter = 0