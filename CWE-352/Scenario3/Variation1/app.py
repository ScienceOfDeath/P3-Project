import sqlite3
from flask import render_template

def init_db():
    pass



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    return render_template("login.html", mode="signup")

@app.route("/login", methods=["POST", "GET"])
def login():

    return render_template("login.html", mode="login")


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
    app.run()