# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import re
import os

# --- Flask App Initialization ---
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

# Diagnostic Print Statements: (You can remove these once everything works)
print(f"Flask App Name: {__name__}")
print(f"Directory of app.py: {os.path.dirname(__file__)}")
print(f"Configured Template Folder Path: {template_dir}")
print(f"Does the configured template folder exist? {os.path.isdir(template_dir)}")
print(f"Does signup.html exist in template folder? {os.path.isfile(os.path.join(template_dir, 'signup.html'))}")


app.secret_key = 'your_super_secret_key_here_please_change_this_in_production'

# --- Database Setup ---
def connect_db(db_name="users.db"):
    """Connects to the SQLite database. Creates it if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the 'users' table in the database if it doesn't already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            profile_picture_path TEXT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            address_line1 TEXT,
            address_city TEXT,
            address_state TEXT,
            address_pincode TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and 'users' table ensured to exist.")

# Call create_tables when the application starts
with app.app_context():
    create_tables()

# --- Helper Functions ---

def hash_password(password):
    """Hashes a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def check_password(password, hashed_password):
    """Checks if a plain text password matches a hashed password."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except ValueError:
        return False

def is_valid_email(email):
    """Checks if the email format is valid using a regular expression."""
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

# --- Flask Routes ---

@app.route('/')
def index():
    """Default route, redirects to signup page."""
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup."""
    if request.method == 'POST':
        # Get data from the signup form
        user_type = request.form['user_type'].strip().capitalize()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        profile_picture_path = request.form.get('profile_picture', '').strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address_line1 = request.form.get('address_line1', '').strip()
        address_city = request.form.get('address_city', '').strip()
        address_state = request.form.get('address_state', '').strip()
        address_pincode = request.form.get('address_pincode', '').strip()

        # Basic server-side validation
        if not all([user_type, first_name, last_name, username, email, password, confirm_password]):
            flash('Please fill in all required fields.', 'error')
            return render_template('signup.html', form_data=request.form)

        if not is_valid_email(email):
            flash('Invalid email format.', 'error')
            return render_template('signup.html', form_data=request.form)

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html', form_data=request.form)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html', form_data=request.form)

        conn = connect_db()
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username or Email already registered. Please choose another or log in.', 'error')
            conn.close()
            return render_template('signup.html', form_data=request.form)

        # Hash the password
        hashed_pwd = hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO users (user_type, first_name, last_name, profile_picture_path, username, email, password_hash, address_line1, address_city, address_state, address_pincode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_type, first_name, last_name, profile_picture_path, username, email, hashed_pwd, address_line1, address_city, address_state, address_pincode)
            )
            conn.commit()
            flash(f'Signup successful for {user_type} {username}! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash(f'Database error during signup: {e}', 'error')
            conn.rollback()
        finally:
            conn.close()
    
    # For GET requests (initial page load) or if POST fails
    # Pass an empty dictionary if it's a GET request to avoid UndefinedError
    return render_template('signup.html', form_data={})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username_or_email = request.form['username_or_email'].strip()
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username_or_email, username_or_email))
        user = cursor.fetchone()

        if user:
            if check_password(password, user['password_hash']):
                session['logged_in'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user['user_type']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                session['email'] = user['email']
                session['profile_picture_path'] = user['profile_picture_path']
                session['address_line1'] = user['address_line1']
                session['address_city'] = user['address_city']
                session['address_state'] = user['address_state']
                session['address_pincode'] = user['address_pincode']

                flash('Login successful!', 'success')
                if user['user_type'] == 'Patient':
                    return redirect(url_for('patient_dashboard'))
                elif user['user_type'] == 'Doctor':
                    return redirect(url_for('doctor_dashboard'))
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('User not found. Please check your username/email or sign up.', 'error')

        conn.close()
    
    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    """Displays the patient dashboard."""
    if not session.get('logged_in') or session.get('user_type') != 'Patient':
        flash('Please log in as a Patient to access this dashboard.', 'error')
        return redirect(url_for('login'))
    
    return render_template('patient_dashboard.html', user=session)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    """Displays the doctor dashboard."""
    if not session.get('logged_in') or session.get('user_type') != 'Doctor':
        flash('Please log in as a Doctor to access this dashboard.', 'error')
        return redirect(url_for('login'))
    
    return render_template('doctor_dashboard.html', user=session)

@app.route('/logout')
def logout():
    """Logs out the user by clearing the session."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

