import os
from flask import Flask, render_template, request, send_file, flash
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)


DOWNLOAD_DIR = "/static"
UPLOAD_DIR = "/static"

@app.route("/")
def index():
    return render_template("index.html")
    pass

@app.route("/fileupload", methods=["POST"])
def upload():
    filename = request.args.get('filename')
    filename.save(os.path.join(UPLOAD_DIR, filename))
    pass


@app.route('/download', methods=["GET", "POST"])
def download():
    
    if request.method == "GET":
        filename = request.args.get('filename')
        
        if not filename:
            flash("File not selected for download")
            return render_template("downloads.html")
        else:
            file_path = os.path.join(DOWNLOAD_DIR, filename)

            return send_file(file_path)

    if request.method == "POST":
        if not filename:
            flash("File not selected for upload")
            return render_template("downloads.html")
        else:
            # Upload Functionality
            pass
         
    else:
        pass


@app.route('/downloads/')
def downloads():
    return render_template("downloads.html")


if __name__ == "__main__":
    app.run()