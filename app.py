import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '.feowkfeopwk3243z,mpo302@;k'

# Track logged in users
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view

# log users out
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
@login_required
def index():
    connection = sqlite3.connect("fetch.db")
    cursor = connection.cursor()
    client_db = cursor.execute("SELECT * FROM clients WHERE user_id = ?", (session["user_id"],)).fetchall()
    name = session.get("name")
    time = datetime.now().hour
    if time < 12:
        greeting = "Good Morning, "
    elif time < 17:
        greeting = "Good Afternoon, "
    elif time > 17:
        greeting = "Good Evening, "
    connection.commit()
    connection.close()
    return render_template("index.html", name=name, greeting=greeting, client=client_db)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Put user entered data in a variable
        email = request.form.get("email").lower()
        password = request.form.get("password").lower()

        # Connect to the database
        connection = sqlite3.connect("fetch.db")
        cursor = connection.cursor()

        # Query the dataabase
        authenticate = cursor.execute("SELECT email, hash FROM users WHERE email = ?", (email,),).fetchone()

        # Error checking
        error = False

        if not email:
            flash("Email must be entered", "email-blank")
            error = True
        
        if not password:
            flash("Password must be entered", "password")
            error = True
        
        if not authenticate:
            flash("Email not found", "email-not-found")
            error = True
        
        else:
            password_check = check_password_hash(authenticate[1], password)
            if password_check == False:
                flash("Password is incorrect. Please try again", "password-check")
                error = True

        if error == False:
            id = cursor.execute("SELECT id FROM users WHERE email = ?", (email,),).fetchone()
            session["user_id"] = id[0]
            db_name = cursor.execute("SELECT name FROM users WHERE id = ?", (session["user_id"],)).fetchone()

            # Remove punctuation from the name string
            name = ''
            for item in db_name:
                name = item

            session["name"] = name
            connection.commit()
            connection.close() 
            return redirect(url_for("index"))

    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        error = False
        # Connect to the database:
        connection = sqlite3.connect("fetch.db")
        cursor = connection.cursor()

        # Get the users name / return an error if blank
        name = request.form.get("name")
        if not name:
            flash("Name must not be blank", "name")
            error = True
        
        # Get the users username / return an error if blank OR if username exists
        username = request.form.get("username").lower()
        if not username:
            flash("Username must not be blank", "username")
            error = True
        db_users = cursor.execute("SELECT username FROM users")
        registered_users = [user[0] for user in db_users]
        if username in registered_users:
            flash("Username already taken", "username")
            error = True
            
        # Get the users email / return an error if blank OR if email exists
        email = request.form.get("email").lower()
        if not email:
            flash("Email must not be blank", "email")
            error = True
        db_email = cursor.execute("SELECT email FROM users")
        registered_email = [email[0] for email in db_email]
        if email in registered_email:
            flash("Email already in use", "email")
            error = True

        # Get the users password and confirm / return an error if blank OR both passwords do not match
        password = request.form.get("password")
        if not password:
            flash("Password must not be blank", "password")
            error = True
        confirm_password = request.form.get("confirm-password")
        if not confirm_password:
            flash("Confirmation of password must not be blank", "confirm-password")
            error = True
        if password != confirm_password:
            flash("Passwords must match", "match-passwords")
            error = True
        password = generate_password_hash(password)

        # If no errors are found, add the user into the database
        if not error:
          cursor.execute("INSERT INTO users(name, username, email, hash) VALUES(?, ?, ?, ?)", (name, username, email, password))
          connection.commit()
          connection.close() 
          return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        error = False
        client = request.form.get("client")
        if not client:
            flash("Client Name Cannot be Blank", "name")
            error = True
        pet_name = request.form.get("pet-name")
        if not pet_name:
            flash("Pets Name Cannot be Blank", "pet")
            error = True
        breed = request.form.get("breed")
        if not breed:
            breed = " "
        age = request.form.get("age")
        if not age:
            age = " "
        gender = request.form.get("gender")
        if not gender:
            gender = " "
        notes = request.form.get("notes")
        if not notes:
            notes = " "    
        if error == False:
            # Connect to the database
            connection = sqlite3.connect("fetch.db")
            cursor = connection.cursor()

            # Add information from form to the database
            cursor.execute("INSERT INTO clients(user_id, client_name, pets_name, breed, age, gender, notes) VALUES(?, ?, ?, ?, ?, ?, ?)", (session["user_id"], client, pet_name, breed, age, gender, notes))
            connection.commit()
            connection.close()
            return redirect(url_for("add"))

    return render_template('add.html')

@app.route('/walks', methods=["GET", "POST"])
@login_required
def walks():
    if request.method == "POST":
        connection = sqlite3.connect("fetch.db")
        cursor = connection.cursor()
        client = request.form.get("client")
        type = request.form.get("type")
        time = request.form.get("time")
        repeat = request.form.get("repeat")
        payment = request.form.get("payment")
        paid = request.form.get("paid")
        notes = request.form.get("notes")
        cursor.execute("INSERT INTO walks(client_id, type, time, repeat, payment, paid, notes) VALUES(?, ?, ?, ?, ?, ?, ?)", (client, type, time, repeat, payment, paid, notes))
        connection.commit()
        connection.close()
    connection = sqlite3.connect("fetch.db")
    cursor = connection.cursor()
    db_clients = cursor.execute("SELECT id, client_name, pets_name, breed FROM clients WHERE user_id = ?", (session["user_id"],)).fetchall()
    connection.commit()
    connection.close()
    return render_template('walks.html', client=db_clients)

if __name__ == "__main__":  
    app.run(debug=True)