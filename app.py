from flask import Flask,render_template ,request,session,url_for,redirect,flash
from attendance import face_detector , Model
from Train import trainclassifier
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import cv2 
from dataset import face_extractor
import datetime



app = Flask(__name__)

app.secret_key = 'xyzsdfg'


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="mysqlpass@123"
app.config['MYSQL_DB']="mydatabase"

mysql = MySQL(app)



@app.route('/')
def home():
  return render_template('index.html')

@app.route('/', methods =['GET', 'POST'])
def login():
    messages = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE email = % s AND password = % s', (email ,password))
        user = cursor.fetchone()
             
        if user:
            session['loggedin'] = True
            session['userid'] = user['Id']
            session['name'] = user['name']
            session['email'] = user['email']
            return redirect('/dashboard')
        else:
            flash('Wrong password/Wrong Email')
            return render_template('index.html')
            
    return render_template('index.html')


  

@app.route('/register', methods =['GET', 'POST'])

def register():
    messages = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            flash('Account already exists !','error')
            return render_template('register.html')
        else:
            sql = "INSERT INTO student (name,email,password) VALUES (% s, % s, % s)"
            values = (userName,email,password)
            cursor.execute(sql,values)
            mysql.connection.commit()
            messages = 'You have successfully registered !'
            return redirect('/')

    
    return render_template('register.html', messages = messages)


# user template
@app.route('/user')
def user():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM studetail')
    studata =cursor.fetchall()
    cursor.close()

    return render_template('user.html' , stud = studata)

@app.route('/insert' ,  methods =['GET', 'POST'])   
def insert():
    if request.method == "POST":
        flash('Data Inserted Successfully!' , 'inserted')
        name = request.form["name"]
        rollno = request.form["rollno"]
        branch = request.form["branch"]
        course = request.form["course"]
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO studetail (name , rollno , branch , Course) VALUES (%s,%s,%s,%s)' , (name ,rollno,branch,course) )
        mysql.connection.commit()
    return redirect('/user' ) 

@app.route('/delete/<string:id_data>' ,  methods =['GET','POST']) 
def delete(id_data): 
    'deleted'
    flash('Data Deleted ' , 'deleted') 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM studetail WHERE Id = %s" , [id_data])
    cursor.execute("ALTER TABLE studetail AUTO_INCREMENT = 1")
    mysql.connection.commit()
    return redirect('/user' )

@app.route('/update/<string:id_data>' ,  methods =['GET','POST']) 
def update(id_data):
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     sql = "SELECT name, rollno, Course, branch FROM studetail WHERE Id = %s"
     cursor.execute(sql, (id_data,))
     existing_data = cursor.fetchone()
     # Render the update form for GET requests
     return render_template('update.html', id_data=id_data, existing_data=existing_data)


@app.route('/process_edit' ,  methods =['GET','POST']) 
def process_edit():

    if request.method == "POST":
         print("Handling POST request")
         id = request.form['id']
         name = request.form["name"]
         rollno = request.form["rollno"]
         course = request.form["course"]
         branch = request.form["branch"]
         flash('Data Updated' , 'updated')
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
         sql = " UPDATE studetail SET name=%s , rollno=%s , Course=%s,  branch=%s WHERE Id = %s" 
         value = (name , rollno,branch ,course ,id)
         cursor.execute(sql,value)
         mysql.connection.commit()
    return redirect(url_for('user') )
    
    # elif request.method == "GET":
    #     # Fetch the existing data for the student
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     sql = "SELECT name, rollno, Course, branch FROM studetail WHERE Id = %s"
    #     cursor.execute(sql, (id_data,))
    #     existing_data = cursor.fetchone()
        
    #     # Render the update form for GET requests
    #     return render_template('update_template.html', id_data=id_data, existing_data=existing_data)

@app.route('/dashboard' ,  methods =['GET', 'POST'])   
def dashboard():
    
    return render_template('dashboard.html')