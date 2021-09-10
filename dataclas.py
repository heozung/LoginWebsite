import array

import mysql.connector
from mysql.connector import errorcode

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root1234",
    database="userinfordb"
)
mycursor = db.cursor()
#mycursor.execute("CREATE TABLE LoginInfo(name VARCHAR(50), occupation VARCHAR(50), phonenumb int, email VARCHAR(100) PRIMARY KEY)")
#mycursor.execute("CREATE TABLE PostSaving(email VARCHAR (100), title VARCHAR (50), contentip LONGTEXT)")
#mycursor.execute("DESCRIBE LoginInfo")
#mycursor.execute("SELECT * FROM LoginInfo")

mycursor.execute("DESCRIBE PostSaving")
for i in mycursor:
    print(i)

#mycursor.execute("TRUNCATE LoginInfo")
for i in mycursor:
    print(i)
#
#mycursor.execute("SELECT occupation FROM LoginInfo WHERE email= 'lenhathungreo@gmail.com' ")
#a = array.array('i')



