from flask import Flask, request, session, render_template_string, render_template, redirect, url_for
import sqlite3
import os
import secrets

app = Flask(__name__)


app.secret_key = secrets.token_hex(32)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            amount DOUBLE NOT NULL
        );
    """)

    db.commit()
    db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/transfer", methods=["POST"])
def transfer():
    if request.method == "POST":
        if "user" not in session:
            return "Unauthorized", 401

        pass
        
    return redirect(url_for("user"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)