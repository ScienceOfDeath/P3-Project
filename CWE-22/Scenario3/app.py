import os
from flask import Flask, render_template, request, send_file, flash

app = Flask(__name__)


DOWNLOAD_DIR = "/static"

@app.route("/")
def index():
    return render_template("index.html")
    pass

@app.route("/fileupload", methods=["POST"])
def upload():
    pass


@app.route('/download', methods=["GET"])
def download():
    filename = request.args.get('filename')
    if not filename:
            flash("File not selected")
            return render_template("downloads.html")
    else:
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        return send_file(file_path)

@app.route('/downloads/')
def downloads():
    return render_template("downloads.html")


if __name__ == "__main__":
    app.run()