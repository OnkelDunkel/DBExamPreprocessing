# Database Exam Project

### Group members: Ali Raza Khan, Mohammed Murad Hossain Sarker, Rasmus Balder Nordbjærg, Yakubu Adeyemi Oseni

## Data importing

### Getting the .txt book files from the Gutenberg Project

We followed the hinted steps creating a VM on DigitalOcean using Vagrant. In the vagrantfile we changed the size of the VM from '1gb' to 's-1vcpu-3gb' because we believed this would better fit our needs.

After for running less than 2 days the script was done and we could download the 5gb archive.tar using scp. Extracting the archive.tar file revealed directory with around 37,000 zipfiles.

### Unzipping the files and putting them into order

We ran below shell commands from the directory of all the zipped files in order to unzip them and thereafter delete the zip files:

    unzip '*.zip'
    rm *.zip

Following commands was used to move files from subfolders to current folder, delete empty folders and show all non-txt files:

	find . -mindepth 2 -type f -print -exec mv {} . \;
	find . -empty -type d -delete
	find -not -iname "*.txt"

Last line gave following ouput. Only few files that aren't .txt:

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

We deleted all the non-txt files:

	find -not -iname "*.txt" -delete

### Getting author and book title from txt

We used below regular expression patterns to extract the author and the book title from the txt files. 

	re_patterns = [
        "[ ]{0,4}Title: (.+)\n\n[ ]{0,4}Author: ([^\n]+)\n",
        "  We need your donations.\n\n\n([^\n]+)\n\nby ([^\n]+)\n\n",
        "\n\nTitle: (.+)\nAuthor: (.+)\nRelease Date: ",
        "\n\n\n\n\n\n[\d]{4}\n\n()\n\nby ()\n\n\nDramatis Personae",
    ]

By testing with a sample of 1000 txt files we concluded that around 5% of the files would be last with our algorithm. This was due to either text encoding not being utf-8 or our regex was not able to extract the book title and author. We agreed that this was an acceptable loss.



### Using the NLP python library spaCy we extracted all named entities from the books

Using the name entity recognition provided by the spaCy library the entities are divided into types so we only included entities of type 'GPE' which should include countries, cities and states.




