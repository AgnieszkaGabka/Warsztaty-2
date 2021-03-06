import argparse
from create_db import User, Message
from psycopg2.errors import UniqueViolation
from models import check_password
from psycopg2 import connect, OperationalError

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password - min 8 characters")
parser.add_argument("-n", "--new_pass", help="new password")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store-true")
args = parser.parse_args()

def new_user(cursor, username, password):
    if len(password) < 8:
        print("Password too short! Has to have at least 8 characters")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User created")
        except UniqueViolation:
            print("User already created before")

def change_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("No such user")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password too short! Has to have at least 8 characters")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print("Password successfully changed")
    else:
        print("Incorrect password")

def delete_user(cursor, username, password, delete):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("No such user")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User sucessfully deleted")
    else:
        print("Incorrect password")

def list_user(cursor):
    users_list = User.load_all_users(cursor)
    for user in users_list:
        print(user.username)

if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            change_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            new_user(cursor, args.username, args.password)
        elif args.list:
            list_user(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError:
        print("Operational Error")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password - min 8 characters")
parser.add_argument("-t", "--to", help="message receiver")
parser.add_argument("-s", "--send", help="message text")
parser.add_argument("-l", "--list", help="list users", action="store_true")

args = parser.parse_args()

def list_messages(cursor, username, password, list):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("No such user")
    elif check_password(password, user.hashed_password):
        messages = Message.load_all_messages(cursor, user.id)
        for message in messages:
            from_ = User.load_user_by_id(cursor, message.from_id)
            print(f"from: {from_.username}")
            print(message.text)
            print(f"data: {message.creation_date}")
    else:
        print("Incorrect password")

def send_message(cursor, username, password, to, send):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("No such user")
    elif check_password(password, user.hashed_password):
        receiver = User.load_user_by_username(cursor, to)
        if not receiver:
            print("No such receiver")
        else:
            if len(send) > 255:
                print("Message too long")
                return
            else:
                message = Message(from_id=username, to_id=to, text=send)
                message.save_to_db(cursor)
                print("Message send")

if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)