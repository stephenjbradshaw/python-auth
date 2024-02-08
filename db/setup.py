import sqlite3

con = sqlite3.connect("auth.db")
cur = con.cursor()
cur.execute("CREATE TABLE user(email, password_hash, verification_token)")
con.close()
