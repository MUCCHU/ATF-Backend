#!./env/bin/python
import mysql.connector
import os
# os.system("./delete_db.py")
mydb = mysql.connector.connect(
    host = "opensoft-1.cwvqdtxsixl6.ap-south-1.rds.amazonaws.com",
    user = "opensoft",
    passwd = "opensoft",
)


my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE users")
# my_cursor.execute("CREATE DATABASE restaurants")
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
my_cursor.execute("USE opensoft")
my_cursor.execute("SHOW TABLES")
for table in my_cursor:
    print(table)
# os.system("./rebuliddb.py")
# os.system("echo Database Rebuilt")