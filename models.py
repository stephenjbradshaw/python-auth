from connection import con
import sqlite3

cur = con.cursor()


def get_user(email: str) -> tuple | None:
    cur.execute("SELECT * FROM user WHERE email=?", (email,))
    res = cur.fetchone()
    return res


def create_user(email: str, salt: str, hashed_password: str, email_verification_token: str) -> tuple:
    data = (email, salt, hashed_password, email_verification_token)
    try:
        cur.execute("INSERT INTO user VALUES(?, ?, ?, ?)", data)
    except sqlite3.IntegrityError as e:
        # Handle silently, as we don't want to reveal which users are already registered
        print("User already exists", e)
    con.commit()


def remove_email_verification_token(email: str):
    '''
    Remove the token, marking the user as verified
    '''
    cur.execute(
        "UPDATE user SET email_verification_token=NULL WHERE email=?", (email,))
    con.commit()


if __name__ == '__main__':
    print(get_user('hello@stephenbradshaw.dev'))
