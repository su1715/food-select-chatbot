import sqlite3
from sqlite3.dbapi2 import connect
conn = sqlite3.connect("foodDic.db")
cur = conn.cursor()

sql = """
    CREATE TABLE foodDicTable (
		indexnum	INTEGER NOT NULL,
		name	TEXT NOT NULL,
    	desert	INTEGER,
    	vietnam	INTEGER,
        taiwan  INTEGER,
        thailand    INTEGER,
        mexico  INTEGER,
        turkey  INTEGER,
        india   INTEGER,
    	occident	INTEGER,
    	japan	INTEGER,
    	china	INTEGER,
    	korea	INTEGER,
    	spicy	INTEGER,
		n_spicy INTEGER,
        cool    INTEGER,
        hot     INTEGER,
        meat    INTEGER,
        soup    INTEGER,
        noodle  INTEGER,
        rice    INTEGER,
        bread   INTEGER,
        veget   INTEGER,
        rice_b  INTEGER,
        sea_f   INTEGER,
        easy    INTEGER,
		priority	INTEGER NOT NULL,
    	PRIMARY KEY(name)
    );"""

cur.execute(sql)
print("foodDicTable has been created.")

conn.commit()
conn.close()