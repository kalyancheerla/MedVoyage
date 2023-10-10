#!/bin/sh

docker run --rm -p 3306:3306 --name mysqlinstance -e MYSQL_ROOT_PASSWORD='pa$$w0rd' -d mysql:latest;
sleep 30;
docker exec -i mysqlinstance mysql -uroot -p'pa$$w0rd' <<EOF
CREATE DATABASE medvoyagedb;
exit
EOF
