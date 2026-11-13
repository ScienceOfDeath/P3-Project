from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/post_comment", methods=["POST"])
def post_comment():

    name = request.form.get("name")
    message = request.form.get("message")

    add_comment(name, message)

    return redirect(url_for("board"))

@app.route("/board", methods=["GET"])
def board():

    rows = get_all_comments()

    return render_template("board.html", comments=rows)


if __name__ == "__main__":
    init_db()
    app.run()