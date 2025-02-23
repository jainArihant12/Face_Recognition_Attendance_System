import mysql.connector



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysqlpass@123",
  database = "mydatabase"
)



mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE studetail (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,rollno VARCHAR(255),name VARCHAR(255),Course VARCHAR(255),branch VARCHAR(255),date VARCHAR(255),time VARCHAR(255),Attendance VARCHAR(255))")

# sql = "INSERT INTO studetail (name, rollno,Course,branch,date,time,Attendance) VALUES (%s, %s,%s, %s,%s, %s,%s)"
# val = ("Rahul", "2","Bsc","None","1-12-22","1:30","Present")
 
# mycursor.execute(sql, val)
# mydb.commit()
 
# print(mycursor.rowcount, "details inserted")
 
# # disconnecting from server
# mydb.close()












