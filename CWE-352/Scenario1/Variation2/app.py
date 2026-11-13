from flask import Flask, request, session, render_template_string, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/user/update-email", methods=["POST"])
def update_email():
    if "user" not in session:
        return "Unauthorized", 401
    pass

 
@app.route("/user/reset-password", methods=["POST"])
def reset_password():
    if "user" not in session:
        return "Unauthorized", 401
    pass

if __name__ == "__main__":
    app.run()