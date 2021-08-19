import sqlite3
from sqlite3.dbapi2 import connect
conn = sqlite3.connect("foodDic.db")
cur = conn.cursor()
sql = """
    CREATE TABLE User (
        userid TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY(userid)
    );
"""

cur.execute(sql)
print("User table has been created.")

conn.commit()
conn.close()
