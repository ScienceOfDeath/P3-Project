from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")


@app.route("/create_user", methods=["POST"])


@app.route("/admin", methods=["POST","GET"])

@app.route("/login", methods=["POST"])


@app.route("/user", methods=["GET"])


@app.route("/admin/reset_password", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)