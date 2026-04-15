from flask import Flask, render_template, request
from flask_cors import CORS
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# DB connection (SQLite)
def get_connection():
    conn = sqlite3.connect("database.db")
    return conn


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login-page')
def login_page():
    return render_template('login.html')


@app.route('/signup-page')
def signup_page():
    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        hashed = generate_password_hash(password)

        conn = get_connection()
        cur = conn.cursor()

        # create table if not exists
        cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")

        try:
            cur.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
            message = "Registered successfully"
        except:
            message = "User already exists"
        finally:
            conn.close()

        return render_template('signup.html', message=message)

    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE email=?", (email,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user[0], password):
        return render_template('login.html', message="Login successful")
    else:
        return render_template('login.html', message="Invalid credentials")


@app.route('/dashboard')
def dashboard():
    return "Welcome to protected page"


if __name__ == "__main__":
    app.run()