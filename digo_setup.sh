

apt update

apt install -y python3-pip
pip3 install spacy
python3 -m spacy download en_core_web_sm
pip3 install json
pip3 install mysql-connector-python
apt install -y unzip

#update link***********************************************************************
wget -O books.zip http://www.mediafire.com/file/2a6b30tg30e901m/books_txts.zip/file
unzip books.zip


#update link*********************************
#wget -O process_books.py http://www.mediafire.com/file/qynfcw0cm2ceyjx/process_books.py/file
#python3 process_books.py
