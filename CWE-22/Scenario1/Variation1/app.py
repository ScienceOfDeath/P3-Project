import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fileupload")
def upload():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)