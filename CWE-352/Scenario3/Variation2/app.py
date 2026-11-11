from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import os
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def init_db():

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
    else:
        return redirect(url_for("user"))
    return render_template("login.html", mode="signup")

@app.route("/login", methods=["POST", "GET"])
def login():

    return render_template("login.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


@app.route("/api-key/generate", methods=["POST"])
def generate_api_key():

    # Implement API Key Generation and all other required prerequisuites here.

    return render_template("dashboard.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)