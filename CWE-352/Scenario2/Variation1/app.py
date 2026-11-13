from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def user():
    pass
 
@app.route("/transfer")
def transfer():
    pass


if __name__ == "__main__":
    app.run()