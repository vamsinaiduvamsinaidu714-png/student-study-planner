from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    user_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (?,?,?)",
            (username,email,password)
        )

        conn.commit()
        conn.close()

        return "User Registered Successfully!"

    return render_template("register.html")
    
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():

    task = request.form['task']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard') 

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    conn.commit()
    conn.close()

    return redirect('/dashboard') 

@app.route('/logout')
def logout():
    return redirect('/')         

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

