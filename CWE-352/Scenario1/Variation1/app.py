from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    pass

@app.route("/user/update-email")
def update_mail():
    pass

 
@app.route("/user/reset-password")
def reset_password():
    pass


if __name__ == "__main__":
    app.run()