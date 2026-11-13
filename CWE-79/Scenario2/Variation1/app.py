from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

ITEMS = [
    "Network Switch",
    "Hardware Security Module",
    "Patch Cable",
    "Rackmount Server",
]


@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
  query = request.args.get("q", "")
  results = [item for item in ITEMS if query.lower() in item.lower()]

  search_template = f"""
    <!doctype html>
    <html>
    <head><title>Search Results</title></head>
    <body>
        <h1>Search Results for: {query}</h1>
        <form action="/search" method="get">
            <input type="text" name="q" value="{query}">
            <button type="submit">Search</button>
        </form>
        <ul>
            {{% for item in results %}}
                <li>{{{{ item }}}}</li>
            {{% else %}}
                <li>No matching items found.</li>
            {{% endfor %}}
        </ul>
        <a href="/">Back</a>
    </body>
    </html>
    """



  return render_template_string(search_template, results=results)


if __name__ == "__main__":
  app.run()