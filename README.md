# Database Exam Project

### Group members: Ali Raza Khan, Mohammed Murad Hossain Sarker, Rasmus Balder Nordbjærg, Yakubu Adeyemi Oseni

We ran below shell command with from the directory of all the zipped books in order to unzip them:

    #unzio all zips
    unzip '*.zip'
    
    #removing all zips
    rm *.zip
    
    #move all files from subfolders to current folder
	find . -mindepth 2 -type f -print -exec mv {} . \;
	
	#delete all empty directories
	find . -empty -type d -delete

	#listin all files not ending with .txt
	find -not -iname "*.txt"

Last line gave following ouput. Not a lot of files that aren't .txt

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

Then running below command to delete the files

	#deleting non-txt files
	find -not -iname "*.txt" -delete








