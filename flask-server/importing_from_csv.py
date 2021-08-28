import sqlite3, csv
import pandas as pd

connection = sqlite3.connect("foodDic.db")
cursor = connection.cursor()

with open('fooddic_new.csv', 'r',encoding='UTF-8') as file :
    no_records = 0
    for row in file:
        if no_records==0:
            connection.commit()
        else:
            cursor.execute('''INSERT into foodDicTable values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row.split(","))
            connection.commit()
        no_records += 1
connection.close()
print("\n{} Records Transferred".format(no_records))