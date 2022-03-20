#!./env/bin/python
import mysql.connector
import os
# os.system("./delete_db.py")
mydb = mysql.connector.connect(
    host = "sql6.freemysqlhosting.net",
    user = "sql6480330",
    passwd = "VxdvywzzhL",
)


my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE users")
my_cursor.execute("CREATE DATABASE restaurants")
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
os.system("./rebuliddb.py")
os.system("echo Database Rebuilt")