from flask import Flask, render_template, request, redirect, session    #session to keep user logged in
import psycopg2     #psycopg2 connect flask to PostgreSQL
from psycopg2.extras import RealDictCursor      #RealDictCursor returns results as dictionaries (easy to use)
from flask_bcrypt import Bcrypt     #bcrypt secure pwd storage (never store plain pwds)

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Change this later to environment variable
app.secret_key = "mysecretkey"

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="taskmanagerdb",
        user="postgres",    # Change if your username is different
        password="Postgres_Password",  # <-- UPDATE THIS
        cursor_factory=RealDictCursor
    )

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    print("✅ /register route is working!")     # Debug print
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            conn.commit()
            cur.close()
            conn.close()
            return "✅ Registration Successful! <a href='/login'>Login here</a>"
        except psycopg2.Error as e:
            return f"❌ Error: {e}"
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and bcrypt.check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return "❌ Invalid username or password"
        
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC", (session["user_id"],))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("dashboard.html", username=session["username"], tasks=tasks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)