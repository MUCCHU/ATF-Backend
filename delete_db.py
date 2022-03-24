#!./env/bin/python
import mysql.connector
mydb = mysql.connector.connect(host = "localhost",user = "root",passwd = "Harsh1606")
my_cursor = mydb.cursor()
my_cursor.execute("DROP DATABASE orders")
# my_cursor.execute("DROP DATABASE restaurants")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

print('*'*10)
print('Database Deleted')
print('*'*10)
