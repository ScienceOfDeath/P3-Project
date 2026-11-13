from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
  pass


@app.route("/search", methods=["GET"])
def search():

  pass


if __name__ == "__main__":
  app.run()