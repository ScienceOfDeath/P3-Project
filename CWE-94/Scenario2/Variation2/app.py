from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

variables = {}

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        var_input = request.form.get("var_def", "").strip()
        calculation = request.form.get("calc", "")

        # TODO: Parse and store user-defined variables (e.g., "vat = 1.25")

        if calculation:
            template_str = f"{{{{ {calculation} }}}}"
            try:
                output = render_template_string(template_str, **variables)
            except Exception as e:
                output = f"Error: {e}"

    return render_template("index.html", output=output, variables=variables)

if __name__ == "__main__":
    app.run(debug=True)