from flask import Flask, render_template, url_for, redirect, jsonify
from db import functions

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/post_comment", methods=["POST"])
def post_comment():

    return redirect(url_for("board"))

@app.route("/api/comments", methods=["GET"])
def api_comments():


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
    app.run()