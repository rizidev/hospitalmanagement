from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hospital_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Create database and table if not exist
def init_db():
    conn = mysql.connection
    cur = conn.cursor()
    # Check if the database exists
    cur.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
    conn.commit()
    # Switch to the new database
    cur.execute("USE hospital_db")
    # Create table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            disease VARCHAR(100),
            phone VARCHAR(15),
            address VARCHAR(255)
        )
    ''')
    conn.commit()
    cur.close()

@app.route('/')
def index():
    init_db()  # Ensure DB and table are initialized
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    cur.close()
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (id, name, age, disease, phone, address) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, name, age, disease, phone, address))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
