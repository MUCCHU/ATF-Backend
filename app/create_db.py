#!./env/bin/python
import mysql.connector
import os
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Harsh1606",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE users")
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
os.system("./rebuliddb.py")
os.system("echo Database Rebuilt")