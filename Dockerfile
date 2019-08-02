FROM mysql:5.6

ADD db_dump.sql /docker-entrypoint-initdb.d/dump.sql

# docker build -f Dockerfile ./ -t dump-mysql:1
# docker run --name dump-mysql --rm -d -p 3306:3306 -e MYSQL_DATABASE=storageofknowledge -e MYSQL_ROOT_PASSWORD=password dump-mysql:1

# docker start fe805dce566b
# docker run --name mysql -d -p 3307:3306 -e MYSQL_DATABASE=storageofknowledge -e MYSQL_ROOT_PASSWORD=password mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
