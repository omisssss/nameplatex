from flask import Flask, render_template, request,flash, redirect,url_for, session
from flask_mysqldb import MySQL
import re
import MySQLdb.cursors

app = Flask(__name__)

# MySQL Configuration
app.secret_key='abcdefg'

app.config['MYSQL_HOST'] = 'localhost'  # Update with your MySQL host
app.config['MYSQL_USER'] = 'root'       # Update with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Update with your MySQL password
app.config['MYSQL_DB'] = 'mydatabase'   # Update with your MySQL database name

mysql = MySQL(app)


# Registration Route
@app.route('/register', methods=['GET','POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'phone_number' in request.form and 'password' in request.form and 'department' in request.form and 'vehicle_type' in request.form and 'vehicle_number' in request.form :
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        department = request.form['department']
        user_type = request.form['user_type']
        vehicle_type = request.form['vehicle_type']
        vehicle_number = request.form['vehicle_number']

        # Create cursor
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE vehicle_number =% s',(vehicle_number,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account Already Exist'
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email):
            mesage='Invalid email'
        elif not re.match(r'^[A-Za-z]{2}\d{2}[A-Za-z]{2}\d{4}$',vehicle_number):
            mesage= 'Invalid vehicle number'    
        elif not vehicle_number or not password or not email:
            mesage = 'please fill out the form'    
        else:
                if user_type=="admin":
                  cursor.execute("INSERT INTO admin(name, email, phone_number, password, department, user_type,vehicle_type,vehicle_number) VALUES( %s,%s, %s, %s, %s, %s, %s,%s)", (name, email, phone_number, password, department,user_type, vehicle_type,vehicle_number))
                else:      
        # Execute query
                 cursor.execute("INSERT INTO users(name, email, phone_number, password, department, user_type,vehicle_type,vehicle_number) VALUES( %s,%s, %s, %s, %s, %s, %s,%s)", (name, email, phone_number, password, department,user_type, vehicle_type,vehicle_number))
        # Commit to database
                mesage = 'you have successfully registered'
                mysql.connection.commit()
       
    elif request.method == 'POST': 
        mesage = 'please fill out the form'  
    return render_template('register.html',mesage=mesage)


# Login Route
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
        #and 'vehicle_number' in request.form and 'TotalAmt' in request.form :
        # Get form data
        email = request.form['email']
        password = request.form['password']
        # Create cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Execute query
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password,))
       # cursor.execute ("SELECT vehicle_number,date, TotalAmt FROM log_table WHERE vehicle_number = %s,%s",(vehicle_number,TotalAmt,))
        #results = cursor.fetchall()
        
        # Fetch user
        user = cursor.fetchall()
        print(user)
        if user:
            # User found, redirect to admin page
            session['loggedin'] = True
            session['email'] = email
            mesage='Logged in successfully'

            return redirect('/user')
        
        else:
            # Invalid credentials, show error message
            mesage = 'Invalid email or password'
    return render_template('login.html',mesage=mesage)



#
# user route
@app.route('/user')
def user():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (session['email'],))
        users = cursor.fetchall()
        # Show the profile page with account info
        return render_template('user.html', users=users)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

# Make Payment route
@app.route('/make_payment', methods=['POST'])
def make_payment():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))

    payment_amount = float(request.form['payment_amount'])

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET total_amt = total_amt + %s WHERE email = %s",
                (payment_amount, email))
    
    mysql.connection.commit()
    cur.close()

    flash("Payment Successful")
    return redirect(url_for('user'))




# adminLogin Route
@app.route('/')
@app.route('/admin', methods=['GET','POST'])
def admin():
    mesage = ''
    if request.method == 'POST' and 'admin_id' in request.form and 'password' in request.form :
        #and 'vehicle_number' in request.form and 'TotalAmt' in request.form :
        # Get form data
        admin_id = request.form['admin_id']
        password = request.form['password']
        #vehicle_number = request.form['vehicle_number']
       # TotalAmt=request.form['TotalAmt']
        
        # Create cursor
        cursor = mysql.connection.cursor()
        
        # Execute query
        cursor.execute("SELECT * FROM admin WHERE admin_id = %s AND password = %s", (admin_id, password,))
       # cursor.execute ("SELECT vehicle_number,date, TotalAmt FROM log_table WHERE vehicle_number = %s,%s",(vehicle_number,TotalAmt,))
        #results = cursor.fetchall()
        
        # Fetch user
        Index = cursor.fetchall()
        
        if Index:
            # User found, redirect to admin page
            session['loggedin'] = True
            session['admin_id'] = admin_id
            mesage = 'Logged in successfully'
           
            return redirect('/index')
    
        else:
            # Invalid credentials, show error message
            mesage = 'Invalid email or password'
    return render_template('admin.html',mesage=mesage)


@app.route('/index')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM users")
    data = cur.fetchall()
    cur.close()
    




    return render_template('index2.html', users=data )


@app.route('/approve/<int:userid>', methods=['GET'])
def approve(userid):
    # Update the user status to "approved" in the database
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET status = %s WHERE userid = %s", ('approved', userid))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('Index'))

@app.route('/reject/<int:userid>', methods=['GET'])
def reject(userid):
    # Update the user status to "rejected" in the database
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET status = %s WHERE userid = %s", ('rejected', userid))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('Index'))




@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        department = request.form['department']
        user_type = request.form['user_type']
        vehicle_type = request.form['vehicle_type']
        vehicle_number = request.form['vehicle_number']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, phone_number, password, department, user_type,vehicle_type,vehicle_number) VALUES( %s,%s, %s, %s, %s, %s, %s,%s)", (name, email, phone_number, password, department,user_type, vehicle_type,vehicle_number))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))


@app.route('/delete/<string:userid>', methods = ['GET'])
def delete(userid):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE userid=%s", (userid,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        userid = request.form['userid']
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        department = request.form['department']
        user_type = request.form['user_type']
        vehicle_type = request.form['vehicle_type']
        vehicle_number = request.form['vehicle_number']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name=%s, email=%s, phone_number=%s, department=%s, user_type=%s, vehicle_type=%s, vehicle_number=%s, status=%s
            WHERE userid=%s
        """, (name, email, phone_number, department, user_type, vehicle_type, vehicle_number, status, userid))
        
        flash("Data Updated Successfully")
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('Index'))  # Add the return statement here
    
    #return render_template('update.html')

#logout Route
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('userid',None)
    session.pop('email',None) 
    return redirect(url_for('login')) 



    

if __name__ == '__main__':
    app.run(debug=True)
















