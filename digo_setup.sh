apt update
apt install -y python3-pip
pip3 install spacy
python3 -m spacy download en_core_web_sm
pip3 install json
pip3 install mysql-connector-python
apt install -y unzip

#set link***********************************************************************
wget -O books.zip link
unzip books.zip
