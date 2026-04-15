from flask import Flask, render_template, request
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

# DB connection function
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

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

        try:
            cur.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
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

    cur.execute("SELECT password FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user['password'], password):
        return render_template('login.html', message="Login successful")
    else:
        return render_template('login.html', message="Invalid credentials")


@app.route('/dashboard')
def dashboard():
    return "Welcome to protected page"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)