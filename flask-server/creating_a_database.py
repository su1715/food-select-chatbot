import sqlite3
from sqlite3.dbapi2 import connect
conn = sqlite3.connect("foodDic.db")
cur = conn.cursor()

sql = """
    CREATE TABLE foodDicTable (
	    name	TEXT NOT NULL,
    	nation	TEXT,
    	spicy	TEXT,
    	temp	TEXT,
    	keyword	TEXT,
    	easy	TEXT,
    	priority	INTEGER,
    	PRIMARY KEY(name)
    );"""

cur.execute(sql)
print("foodDicTable has been created.")

conn.commit()
conn.close()