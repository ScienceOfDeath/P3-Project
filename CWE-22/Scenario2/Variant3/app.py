from flask import Flask, request, render_template
import os
app = Flask(__name__)


FILES_DIR = "static"

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/view_file/", methods = ["POST"])
def view_file():
    filename = request.form.get("file")
    file_path = os.path.join(FILES_DIR, filename)
    try:
        with open(file_path, "r") as f:            
            content = f.read()
        return render_template("view_file.html", content=content)
    except Exception as e:
        return render_template("view_file.html",content=f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)