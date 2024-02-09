import sqlite3
import os

if os.environ.get("ENV") == "test":
    con = sqlite3.connect("test.db")
else:
    con = sqlite3.connect("auth.db")
