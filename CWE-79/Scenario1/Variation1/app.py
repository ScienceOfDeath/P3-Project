from flask import Flask, render_template, url_for, request, redirect
from db import add_comment, get_all_comments

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/board", methods=["POST"])
def post_comment():
    return redirect(url_for("show_comments"))


@app.route("/comments", methods=["GET"])
def show_comments():
    return render_template("comments.html")


if __name__ == "__main__":
    app.run()