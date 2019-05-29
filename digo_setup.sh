

#update link***********************************************************************
wget -O books.zip http://www.mediafire.com/file/2a6b30tg30e901m/books_txts.zip/file
apt install -y unzip
unzip books.zip

apt install -y python3-pip
pip3 install spacy
python3 -m spacy download en_core_web_sm
pip3 install json
pip3 install mysql-connector-python

#update link*********************************
wget -O process_books.py http://www.mediafire.com/file/ceqpp37gijcy3ad/process_cities.py/file

python3 process_books.py
