from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from app import predict_bp

app = Flask(__name__)
app.secret_key = 'your_main_secret_key' # Secret key for the main app
app.register_blueprint(predict_bp, url_prefix='/prediction')

# Connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',        # Your MySQL username
        password='252179',  # Your MySQL password
        database='user_db'    # Your database name
    )
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index1.html')

# Sign up route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                           (username, password, email))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('sign_in'))
        except mysql.connector.Error as err:
            flash(f"Error during sign up: {err}", category='error')
            if conn.is_connected():
                conn.rollback()
            if cursor.is_open():
                cursor.close()
            if conn.is_connected():
                conn.close()

    return render_template('sign_up.html')

# Sign in route
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            # Redirect to the prediction blueprint's index route
            return redirect(url_for('predict.index'))
        else:
            return 'Invalid credentials'

    return render_template('sign_in.html')

if __name__ == '__main__':
    app.run(debug=True)