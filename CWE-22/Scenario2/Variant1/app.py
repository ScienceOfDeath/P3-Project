import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    pass

# File Upload Functionality


# File Download Functionality


if __name__ == "__main__":
    app.run(debug=True)