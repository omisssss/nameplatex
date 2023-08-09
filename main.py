
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import re
import MySQLdb.cursors
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)

# MySQL Configuration
app.secret_key = 'abcdefg'

app.config['MYSQL_HOST'] = 'localhost'  # Update with your MySQL host
app.config['MYSQL_USER'] = 'root'       # Update with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Update with your MySQL password
app.config['MYSQL_DB'] = 'mydatabase'   # Update with your MySQL database name

mysql = MySQL(app)


def send_email(to_email, subject, message):
    sender_email = 'nehashinge74@gmail.com'  # Update with your Gmail email address
    sender_password = 'Neha@shinge21'  # Update with your Gmail password

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.close()
        print('Email sent successfully')
    except Exception as e:
        print('Error sending email:', str(e))


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'phone_number' in request.form and 'password' in request.form and 'department' in request.form and 'vehicle_type' in request.form and 'vehicle_number' in request.form:
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
        cursor.execute('SELECT * FROM users WHERE vehicle_number = %s', (vehicle_number,))
        account = cursor.fetchone()
        if account:
            message = 'Account Already Exist'
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            message = 'Invalid email'
        elif not re.match(r'^[A-Za-z]{2}\d{2}[A-Za-z]{2}\d{4}$', vehicle_number):
            message = 'Invalid vehicle number'
        elif not vehicle_number or not password or not email:
            message = 'Please fill out the form'
        else:
            if user_type == "admin":
                cursor.execute("INSERT INTO admin(name, email, phone_number, password, department, user_type,vehicle_type,vehicle_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                               (name, email, phone_number, password, department, user_type, vehicle_type, vehicle_number))
            else:
                # Execute query
                cursor.execute("INSERT INTO users(name, email, phone_number, password, department, user_type,vehicle_type,vehicle_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                               (name, email, phone_number, password, department, user_type, vehicle_type, vehicle_number))
            
            # Commit to database
            mysql.connection.commit()

            # Send email with user ID and password
            subject = 'Registration Details'
            message = f'Your user ID is: {email}\nYour password is: {password}'
            send_email(email, subject, message)

            message = 'You have successfully registered. Check your email for login details.'

    elif request.method == 'POST':
        message = 'Please fill out the form'

    return render_template('register.html', message=message)
    

if __name__ == '__main__':
    app.run(debug=True)
