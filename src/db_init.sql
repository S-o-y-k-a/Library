
CREATE USER lib_user WITH PASSWORD 'pass';

CREATE DATABASE library;

ALTER DATABASE library OWNER to lib_user;