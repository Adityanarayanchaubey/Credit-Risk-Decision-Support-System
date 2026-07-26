import sqlite3
import pandas as pd

#read csv file
df1=pd.read_csv("data/raw/borrower_profiles.csv")
df2=pd.read_csv("data/raw/loan_applications.csv")

#Create SQLite database
conn=sqlite3.connect("data/loan_default.db")

# Load table
df1.to_sql("borrower_profiles",conn, if_exists="replace", index=False)
df2.to_sql("loan_applications", conn, if_exists="replace", index=False)

conn.close()

print("database created successfully")