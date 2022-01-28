from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase

sql1 = """CREATE DATABASE Users;"""

sql2 = """CREATE TABLE users
(
    id serial primary key,
    username varchar(255),
    hashed_password varchar(80)
);"""

sql3 = """CREATE TABLE messages
(
    id serial primary key,
    from_id int NOT NULL,
    to_id int NOT NULL,
    creation_date timestamp default current_timestamp,
    text varchar(255),
    FOREIGN KEY (from_id)
    REFERENCES users(id),
    FOREIGN KEY (to_id)
    REFERENCES users(id)
);"""

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"

cnx = connect(user=USER, host=HOST, password=PASSWORD)
cnx.autocommit = True
cursor = cnx.cursor()
try:
    cursor.execute(sql1)
    print("Database Users created")
except DuplicateDatabase:
    print("Database already created")

cnx.close()