from flask import Flask, request, render_template
app = Flask(__name__)


FILES_DIR = "static"

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/view_file/")
def view_file():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)