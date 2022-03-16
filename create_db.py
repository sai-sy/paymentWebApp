import mysql.connector
import imbedded as i

mydb = mysql.connector.connect(
    host = i.s.hst,
    user=i.s.usr,
    passwd=i.s.psswd
)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE main")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)