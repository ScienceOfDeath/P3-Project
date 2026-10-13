from flask import Flask, render_template

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

@app.route("/user", methods=["POST","GET"])
def user():
    return render_template("user.html")

@app.route("/admin/reset_password", methods=["POST"])
def reset_password():
    return render_template("admin_panel.html")

if __name__ == "__main__":
    app.run(debug=True)