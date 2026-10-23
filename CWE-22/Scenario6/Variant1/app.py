from flask import Flask, request, render_template, safe_join, abort
import os
app = Flask(__name__)


FILES_DIR = "static"

@app.route("/", methods = ["GET"])
def main():
    return render_template("index.html")

app = Flask(__name__)
UPLOAD_DIRECTORY = "/static"


@app.route("/view_file/", methods=[""])
def view_file():
  filename = request.form.get("file")
  file_path = safe_join(UPLOAD_DIRECTORY, filename)

  if not file_path or not os.path.exists(file_path) or not os.path.isfile(file_path):
    abort(404)

  try:
    with open(file_path, "r") as f:
      content = f.read()
    return render_template("view_file.html", content=content)
  except Exception:
    abort(500)
