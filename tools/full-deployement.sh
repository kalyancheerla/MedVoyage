#!/bin/sh

# MySQL Setup
docker run -d --rm -p 3306:3306 --name mysqlinstance -e \
       MYSQL_ROOT_PASSWORD='pa$$w0rd' -d mysql:latest
sleep 30;
docker exec -i mysqlinstance mysql -uroot -p'pa$$w0rd' <<EOF
CREATE DATABASE medvoyagedb;
exit
EOF


# Clone the MedVoyage Repo
cd $HOME
rm -rf MedVoyage
git clone git@github.com:kalyancheerla/MedVoyage.git

PROJECT_PATH=$HOME/MedVoyage
SRC_PATH=$PROJECT_PATH/src


# Set .env file
cp $HOME/.env $SRC_PATH/


# Collect and Serve static files
cd $PROJECT_PATH
python3 -m venv venv
cd $SRC_PATH
$PROJECT_PATH/venv/bin/pip install -r requirements.txt
$PROJECT_PATH/venv/bin/python manage.py collectstatic
rm -rf /var/www/html/medvoyage/
cp -r $SRC_PATH/static /var/www/html/medvoyage/


# Build and Run the MedVoyage container
cd $SRC_PATH
docker build -t medvoyage .
docker run --rm -d --name medvoyage -p 8000:8000 medvoyage:latest
