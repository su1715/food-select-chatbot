import sqlite3
from sqlite3.dbapi2 import connect
conn = sqlite3.connect("foodDic.db")
cur = conn.cursor()
sql = """
    CREATE TABLE User_history (
        userid TEXT NOT NULL,
        search_index INTEGER,
        country  text,
        ingredient text,
        temperature text,
        spicy text,
        simple text, 
        PRIMARY KEY(userid)
    );  
"""

cur.execute(sql)
print("User_history table has been created.")

conn.commit()
conn.close()
