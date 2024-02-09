from db.connection import con
import sqlite3
from typing import Optional

cur = con.cursor()


class User:
    def __init__(self, email: str, salt: str, hashed_password: str, email_verification_token: str | None):
        self.email = email
        self.salt = salt
        self.hashed_password = hashed_password
        self.email_verification_token = email_verification_token

    def __str__(self):
        return f"User(email: {self.email}, salt: {self.salt}, hashed_password: {self.hashed_password}, email_verification_token: {self.email_verification_token})"


def get_user_by_email(email: str) -> Optional[User]:
    cur.execute("SELECT * FROM user WHERE email=?", (email,))
    row = cur.fetchone()
    if row:
        return User(*row)
    else:
        return None


def create_user(user: User) -> tuple:
    data = (user.email, user.salt, user.hashed_password,
            user.email_verification_token)
    try:
        cur.execute("INSERT INTO user VALUES(?, ?, ?, ?)", data)
    except sqlite3.IntegrityError as e:
        # Handle silently, so as not to reveal which users are already registered
        print("User already exists:", e)
    con.commit()


def remove_email_verification_token(email: str):
    '''
    Remove the token, marking the user as verified
    '''
    cur.execute(
        "UPDATE user SET email_verification_token=NULL WHERE email=?", (email,))
    con.commit()
