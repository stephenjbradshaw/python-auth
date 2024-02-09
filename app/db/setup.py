import sqlite3
import os


def init_db():
    '''
    Connect to database and create required table.
    When testing, recreate the test database
    '''
    if os.environ.get("ENV") == "test":
        con = sqlite3.connect("test.db")
    else:
        con = sqlite3.connect("auth.db")

    cur = con.cursor()
    cur.execute(
        "CREATE TABLE user(email STRING UNIQUE NOT NULL, salt STRING NOT NULL, password_hash STRING NOT NULL, email_verification_token STRING)")
    con.close()


if __name__ == '__main__':
    init_db()
