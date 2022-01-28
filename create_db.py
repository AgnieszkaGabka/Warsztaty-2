from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

sql1 = """CREATE DATABASE users;"""

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

try:
    cnx = connect(user=USER, host=HOST, password=PASSWORD)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(sql1)
        print("Database users created")
    except DuplicateDatabase:
        print("Database already created")
except OperationalError:
    print ("Operational Error")

cnx.close()

try:
    cnx = connect(user=USER, host=HOST, password=PASSWORD, database="users")
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(sql2)
        print("Table users created")
    except DuplicateTable:
        print("Table users already created")
except OperationalError:
    print ("Operational Error")

cnx.close()

try:
    cnx = connect(user=USER, host=HOST, password=PASSWORD, database="users")
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(sql3)
        print("Table messages created")
    except DuplicateTable:
        print("Table messages already created")
except OperationalError:
    print ("Operational Error")

cnx.close()