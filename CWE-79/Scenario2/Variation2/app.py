from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)


# Items should be stored in an sqlite3 database
ITEMS = [""]


@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = [item for item in ITEMS if query.lower() in item.lower()]


    # Create the search template
    search_template = f""""""



    return render_template_string(search_template, results=results)


if __name__ == "__main__":
  app.run()