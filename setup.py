import sqlite3

'''
Connect to database and create required table

'''
con = sqlite3.connect("auth.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE user(email STRING UNIQUE, salt, password_hash, email_verification_token)")
con.close()
