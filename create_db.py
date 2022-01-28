from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable
from models import hash_password, generate_salt, check_password

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

class User
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user.id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

class Message
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text)
                            VALUES(%s, %s, %s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()['id']
            self.creation_date = cursor.fetchone()['timestamp']
            return True
        else:
            sql = """UPDATE Users SET from_id=%s, to_id=%s, text=%s
                           WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        messages = []
        if user_id is not None:
            sql = "SELECT id, from_id, to_id, text, FROM Message"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, FROM Message"
            cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message._creation_date = creation_date
            loaded_message.text = text
            messages.append(loaded_message)
        return messages