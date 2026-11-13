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
    if "username" not in session:
        return render_template("login.html")
    return render_template("user.html", username=session["name"])

@app.route("/admin", methods=["GET"])
def admin():
    if session.get("username") != "admin":
        return render_template("admin_login.html")
    return render_template("admin.html", username=session["admin"])

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == db_username and password == db_password:
            session["user"] = username
            return redirect(url_for("user"))
        return render_template("login.html", error="Wrong username or password")
    return render_template("login.html")

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == db_username and password == db_password:
            session["admin_user"] = username
            return redirect(url_for("admin"))
        return render_template("admin_login.html", error="Wrong username or password")
    return render_template("admin_login.html")

@app.route("/admin/reset_password", methods=["POST", "GET"])
def reset_password():
    return render_template("admin_reset.html")

if __name__ == "__main__":
    app.run()