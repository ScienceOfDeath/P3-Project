from flask import Flask, request, render_template, abort
import os
app = Flask(__name__)

FILES_DIR = "static"

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/view_file/", methods=["POST"])
def view_file():
  filename = request.form.get("file")
  file_path = os.path.join(FILES_DIR, filename)

  if not file_path or not os.path.exists(file_path) or not os.path.isfile(file_path):
    abort(404)

  try:
    with open(file_path, "r") as f:
      content = f.read()
    return render_template("view_file.html", content=content)
  except Exception:
    abort(500)


if __name__ == "__main__":
  app.run(debug=True)