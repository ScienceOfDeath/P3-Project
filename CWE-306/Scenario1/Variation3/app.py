from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user", methods=["POST", "GET"])
def create_user():
    return render_template("create_user.html")

@app.route("/user", methods=["GET"])
def user():
    return render_template("user.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    return render_template("admin_login.html")

@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    return render_template("reset_panel.html")

if __name__ == "__main__":
    app.run(debug=True)