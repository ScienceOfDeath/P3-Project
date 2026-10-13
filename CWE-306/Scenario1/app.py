from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    return render_template("create_user.html")

@app.route("/admin", methods=["POST","GET"])
def admin():
    return render_template("admin.html")

@app.route("/login", methods=["POST"])
def login():
    user=request.args.get('name')
    password=request.args.get('password')
    return render_template(url_for("user"))

@app.route("/user", methods=["GET"])
def user(name):
    return render_template("user.html",user=name)

@app.route("/admin/reset_password", methods=["POST"])
def reset_password():
    return render_template("admin_panel.html")

if __name__ == "__main__":
    app.run(debug=True)