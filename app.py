from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

import re

def sanitize_input(user_input):
    # Replace & with &amp;
    sanitized = re.sub(r'&', '&amp;', user_input)
    # Replace < with &lt;
    sanitized = re.sub(r'<', '&lt;', sanitized)
    # Replace > with &gt;
    sanitized = re.sub(r'>', '&gt;', sanitized)
    # Replace " with &quot;
    sanitized = re.sub(r'"', '&quot;', sanitized)
    # Replace ' with &#x27; (hexadecimal for apostrophe)
    sanitized = re.sub(r"'", '&#x27;', sanitized)
    # Replace occurrences of "script" with a safe alternative
    sanitized = re.sub(r'script', '&#x73;cript', sanitized, flags=re.IGNORECASE)
    return sanitized



# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                profile_pic_url TEXT
            )
        ''')
    conn.close()

# Initialize database
init_db()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('profile', identifier=session['username']))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = sanitize_input(request.form['username'])
        password = sanitize_input(request.form['password'])
        try :
            profile_pic_url = sanitize_input(request.form['profile_pic_url'])
        except:
            profile_pic_url = "https://pbs.twimg.com/profile_images/1735030914382749699/iwS0_jHR_400x400.jpg"

        conn = get_db_connection()
        try:
            with conn:
                conn.execute('INSERT INTO users (username, password, profile_pic_url) VALUES (?, ?, ?)',
                             (username, generate_password_hash(password), profile_pic_url))
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already taken. Please choose a different one.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('profile', identifier=user['username']))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/profile/<identifier>')
def profile(identifier):
    conn = get_db_connection()
    if identifier.isdigit():
        user = conn.execute('SELECT * FROM users WHERE id = ?', (int(identifier),)).fetchone()
    else:
        user = conn.execute('SELECT * FROM users WHERE username = ?', (identifier,)).fetchone()
    conn.close()

    if user:
        return render_template('profile.html', username=user['username'], profile_pic_url=user['profile_pic_url'])
    else:
        return 'User not found', 404

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        url = request.form['url']
        flag_cookie = 'flag=your_flag_here'  # Replace with your actual flag

        try:
            response = requests.get(url, cookies={'flag': flag_cookie})
            if response.status_code == 200:
                flash('Request successful. Check your URL for the flag!')
            else:
                flash(f'Request failed with status code: {response.status_code}')
        except requests.RequestException as e:
            flash(f'An error occurred: {e}')

        return redirect(url_for('report'))
    return render_template('report.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
