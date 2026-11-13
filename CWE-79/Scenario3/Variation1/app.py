from flask import Flask, render_template, url_for, request, redirect, jsonify
from db import add_comment, get_all_comments, init_db

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/post_comment", methods=["POST"])
def post_comment():

    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    add_comment(name, message)

    return redirect(url_for("board"))

@app.route("/api/comments", methods=["GET"])
def api_comments():
    rows = get_all_comments()

    comments = [
        {
            "name": row["name"],
            "message": row["message"]
        }
        for row in rows
    ]
    return jsonify(comments)

@app.route("/board", methods=["GET"])
def board():
    
    return render_template("board.html")


if __name__ == "__main__":
    init_db()
    app.run()