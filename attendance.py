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

@app.route('/dataset')
def dataset():
    
    return render_template('dataset.html')


@app.route('/capture', methods=['POST'])
def generate_frames():
    cap = cv2.VideoCapture(0)
    count = 0
    idofstudent = int(request.form['student-id'])
    while True:
        ret, frame = cap.read()

        if face_extractor(frame) is not None:
            count += 1
            face = cv2.resize(face_extractor(frame), (500, 500))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = f'facephoto/user.{idofstudent}.{count}.jpg'
            cv2.imwrite(file_name_path, face)

            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('face cropper',face)
        else:
            print("Face not found (^_^)")
            pass

        if cv2.waitKey(1) == 13 or count == 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Dataset collection complete")
    return "dataset complete"
    

@app.route('/Train')
def train():
    return render_template('Train.html')

@app.route('/traindone', methods=['POST'])
def traindone():
    trainclassifier()
    return render_template('Train.html', message='Training completed successfully.')

@app.route('/attendance')
def attend():
    return render_template('attendance.html')


@app.route('/detection',methods=['POST'])
def detection():

    cap = cv2.VideoCapture(0)
    match_found = False
    while True:

      ret, frame = cap.read()

      image, face = face_detector(frame)
    

      try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        id ,result = Model.predict(face)
        confidence = int(100*(1-(result)/300))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT name FROM studetail WHERE Id = %s",(id,))
        student_data = cursor.fetchone()
        student_name = student_data['name']
        print(student_name)
        print(confidence)
        attendance = "Absent"
        
        if confidence > 72:
            cv2.putText(image,f'Name:{student_name}', (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Face Cropper', image)
            if not match_found:
                current_time = datetime.datetime.now()
                date = current_time.date()
                time = current_time.time()
                print(date)
                attendance = "Present"
                cursor.execute("UPDATE studetail SET date = %s, time = %s , Attendance =%s WHERE Id = %s", (date, time,attendance,id))
                mysql.connection.commit() 
                match_found = True

                
           
    

        else:
            cv2.putText(image, "Unknown", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Cropper', image)


      except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass

      if cv2.waitKey(1)==13:
        break


    cap.release()
    cv2.destroyAllWindows()
    return render_template('attendance.html')

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    date = request.form['date']
    time = request.form['time']
    # Perform any necessary processing with date and time here
    # For example, you can store them in a database
    
    # Then render user.html and pass date and time as template variables

    return render_template('user.html', date=date, time=time)

    
if __name__ == '__main__':
    app.run(debug=True) 
