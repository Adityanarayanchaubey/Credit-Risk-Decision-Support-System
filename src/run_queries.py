import sqlite3

conn=sqlite3.connect("data/loan_default.db")

with open("sql/queries.sql","r") as file:
    query=file.read()

cursor=conn.cursor()
cursor.execute(query)

rows=cursor.fetchall()

for row in rows:
    print(row)

conn.close()