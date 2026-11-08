from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user", methods=["POST", "GET"])
def create_user():
    #TO DO:
    #Create a create user panel where a user can sign up 
    return render_template("create_user.html")

@app.route("/user", methods=["GET"])
def user():
    #TO DO:
    #Create user panel where user is redirected after login in
    return render_template("user.html")

@app.route("/admin", methods=["GET"])
def admin():
    #TO DO:
    #Create admin panel where admins are redirected after login and have the option to press reset password button which function resides at reset panel
    return render_template("admin.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    #TO DO:
    #Create a page where users can login and check if username and password matches a user in database
    return render_template("login.html")

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    #TO DO:
    #Create a page where admins can login and check if username and password matches admin user in database
    return render_template("admin_login.html")

@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    #TO DO:
    #Create a page where you can reset a users password
    return render_template("reset_panel.html")

if __name__ == "__main__":
    app.run(debug=True)