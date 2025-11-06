from flask import Flask, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Change this later to environment variable
app.secret_key = "mysecretkey"

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="taskmanagerdb",
        user="postgres",    # Change if your username is different
        password="Your_Postgres_Password",  # <-- UPDATE THIS
        cursor_factory=RealDictCursor
    )

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)