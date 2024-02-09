import sqlite3

'''
Connect to database and create required table

'''
con = sqlite3.connect("auth.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE user(email STRING UNIQUE NOT NULL, salt STRING NOT NULL, password_hash STRING NOT NULL, email_verification_token STRING)")
con.close()

