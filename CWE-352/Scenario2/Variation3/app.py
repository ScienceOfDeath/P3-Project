from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import os
import sqlite3
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def login_required(f):
    @wraps(f)
    def login_required_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return login_required_function


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance DOUBLE NOT NULL
        );
    """)

    db.commit()
    db.close()

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if not (2 <= len(username) <= 32) or not username.replace("_", "").isalnum():
            flash("Username must be 2-32 letters and only letters, numbers and underscore")
        elif len(password) < 4:
            flash("Password must be more than 3 letters")
        else:
            db = get_db()
            try:
                db.execute("INSERT INTO users (username, email, password, balance) VALUES (?,?,?, 0)", (username, email, generate_password_hash(password)))
                db.commit()
            except sqlite3.IntegrityError:
                flash("That username is taken.")
            else:
                user = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("user"))
    return render_template("login.html", mode="signup")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        row = get_db().execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if row and check_password_hash(row["password"], password):
            session.clear()
            session["user_id"] = row["id"]
            return redirect(url_for("user"))
        flash("Wrong username or password!")

    return render_template("login.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/user")
@login_required
def user():
    balance = get_db().execute("SELECT balance FROM users WHERE id=?", (session["user_id"],)).fetchone()
    return render_template("user.html", balance=balance)

@app.route("/transfer", methods=["POST"])
def transfer():

    # Implement transfer logic here

    pass

if __name__ == "__main__":
    init_db()
    app.run(debug=True)